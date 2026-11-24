"""Word timings for the Mark VO: silence-segmented zipformer ASR, segment onsets from the energy envelope,
aligned to the script; inserts extra pause at section breaks and writes the stretched VO."""
import sherpa_onnx, soundfile as sf, numpy as np, json, re, subprocess, difflib
EXTRA = 0.30  # added silence at each section break
D='/home/claude/models/sherpa-onnx-zipformer-gigaspeech-2023-12-12/'
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=D+'encoder-epoch-30-avg-1.onnx',decoder=D+'decoder-epoch-30-avg-1.onnx',
    joiner=D+'joiner-epoch-30-avg-1.onnx',tokens=D+'tokens.txt',num_threads=2,decoding_method='greedy_search')
a,sr=sf.read('vo/vo16.wav',dtype='float32')
H=int(0.01*sr)
db=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+H]**2))+1e-9) for i in range(0,len(a)-H,H)])
def onset(t): # first 10ms frame from t with energy > -45 dB
    i=int(t/0.01)
    while i<len(db) and db[i]<-38: i+=1
    return i*0.01
def offset(t): # last loud frame before t
    i=int(t/0.01)
    while i>0 and db[i]<-45: i-=1
    return (i+1)*0.01
out=subprocess.run(['ffmpeg','-i','vo/vo16.wav','-af','silencedetect=noise=-38dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; se=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
mids=[(x+y)/2 for x,y in zip(ss,se)]
cuts=[0.0]+mids+[len(a)/sr]
asr=[]  # [word, start, segment_index, pieces]
def decode(t0,t1):
    seg=a[int(t0*sr):int(t1*sr)]
    st=rec.create_stream(); st.accept_waveform(sr,seg); rec.decode_stream(st); r=st.result
    ws=[]
    for tok,ts in zip(r.tokens,r.timestamps):
        if tok.startswith((' ','▁')) or not ws: ws.append([tok.strip(' ▁'),t0+ts,[(tok.strip(' ▁'),t0+ts)]])
        else: ws[-1][0]+=tok; ws[-1][2].append((tok,t0+ts))
    return ws
N=len(cuts)-1
for k in range(N):
    c0,c1=cuts[k],cuts[k+1]
    w0=cuts[max(0,k-1)]; w1=cuts[min(N,k+2)]
    ws=[w for w in decode(w0,w1) if c0<=w[1]<c1]
    # the first word of the whole file has no left context: anchor it to the energy onset
    if k==0 and ws: ws[0][1]=onset(0.0)
    asr+=[[w[0],w[1],k,w[2]] for w in ws]
script=[]
for ln in json.load(open('vo/script_lines.json')):
    for i,w in enumerate(ln['text'].split(' ')): script.append((ln['id'],i,w))
norm=lambda w: re.sub(r"[^a-z']",'',w.lower())
A=[norm(w[0]) for w in asr]; S=[norm(w[2]) for w in script]
sm=difflib.SequenceMatcher(a=S,b=A,autojunk=False)
times=[None]*len(S); log=[]
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='equal':
        for d in range(i2-i1):
            j=j1+d; k=asr[j][2]
            first = (j==0) or asr[j-1][2]!=k
            # transducer emits a chunk's first token early (during the pause): use the energy onset instead;
            # other tokens lead the audio slightly, so nudge them later
            times[i1+d]= asr[j][1]+0.05
    else:
        log.append((op,S[i1:i2],A[j1:j2]))
        # spread the script words over the asr span (e.g. "a sign" heard as "assigned")
        if j2>j1:
            t0=asr[j1][1]; pcs=[p for w in asr[j1:j2] for p in w[3]]
            for d in range(i2-i1):
                times[i1+d]=pcs[min(len(pcs)-1, round(d*len(pcs)/(i2-i1)))][1]
print('diffs:',log)
# words the ASR missed: place them between their neighbours, just before the next word
for k in range(len(times)):
    if times[k] is None:
        j=k
        while times[j] is None: j+=1
        prev=times[k-1]; nxt=times[j]; n=j-k
        for d in range(n): times[k+d]=max(prev+0.08, nxt-0.16*(n-d))
assert all(t is not None for t in times)
def syl(w):
    w=re.sub('[^a-z]','',w.lower()); m=len(re.findall('[aeiouy]+',w)) or 1
    return max(1,m-1 if len(w)>3 and w.endswith('e') and not w.endswith('le') and m>1 else m)
# a word stamped inside a pause really starts when the pause ends (the transducer emits early across silence)
for k in range(len(times)):
    for x,y in zip(ss,se):
        if x <= times[k] < y:
            # just past the pause start: it is the tail of the last word; otherwise it is the next phrase's first word
            after_pause = script[k][1]==0 or re.search(r'[.,]$', script[k-1][2]) is not None
            times[k] = y if after_pause else x-0.12
    if k==0: times[k]=onset(0.0)
for k in range(1,len(times)):
    if script[k][0]==script[k-1][0]:
        times[k]=max(times[k], times[k-1]+0.08+0.07*syl(script[k-1][2]))
# section-break shifts
breaks=[0]+[k for k,(lid,i,w) in enumerate(script) if i==0 and (lid[1]=='1' and lid!='k1')]  # first line of each section
import os
LX=json.load(open('vo/line_extra.json')) if os.path.exists('vo/line_extra.json') else {}
starts_new_sec=set(k for k,(lid,i,w) in enumerate(script) if i==0 and lid in ('h1','r1','e1','d1','i1','c1'))
# gap amount inserted before word k
gap=[0.0]*len(S)
for k in range(1,len(S)):
    if script[k][1]==0:  # first word of a line
        gap[k]=(EXTRA if k in starts_new_sec else 0.0)+LX.get(script[k-1][0],0.0)
shift=list(np.cumsum(gap))
# build per-line [start,end]
res={}; prev=None
for k,(lid,i,w) in enumerate(script):
    s0=times[k]
    if k+1<len(S) and script[k+1][0]==lid: e0=times[k+1]
    else:
        nxt = times[k+1] if k+1<len(S) else len(a)/sr
        sil=[x for x in ss if s0<x<nxt]
        e0=offset(sil[0]) if sil else offset(nxt-0.02)
        e0=max(e0,s0+0.12)
    res.setdefault(lid,[]).append([round(s0+shift[k],3),round(e0+shift[k],3)])
json.dump(res,open('vo/vo_words.json','w'),indent=0)
# stretched VO: insert EXTRA s of silence at the midpoint of the pause before each new section
ins=[]; amt=[]
for k in range(len(S)):
    if gap[k]>0:
        t=times[k]; cand=[m for m in mids if m<t]; ins.append(max(cand)); amt.append(gap[k])
segs=[]; prevc=0.0
fl=[]; 
for n,c in enumerate(ins+[None]):
    end = f':end={c:.4f}' if c is not None else ''
    fl.append(f"[0]atrim=start={prevc:.4f}{end},asetpts=PTS-STARTPTS[p{n}]")
    if c is not None: fl.append(f"anullsrc=r=44100:cl=mono,atrim=0:{amt[n]:.3f}[z{n}]")
    prevc=c if c is not None else prevc
order=''.join(f'[p{n}]'+(f'[z{n}]' if n<len(ins) else '') for n in range(len(ins)+1))
cnt=len(ins)*2+1
fl.append(f"{order}concat=n={cnt}:v=0:a=1[o]")
subprocess.run(['ffmpeg','-v','error','-y','-i','vo/mark_vo.mp3','-filter_complex',';'.join(fl),'-map','[o]','-ar','48000','vo/vo_stretched.wav'],check=True)
print('inserted',[(round(x,2),round(y,2)) for x,y in zip(ins,amt)])
