import json, subprocess, re
W=json.load(open('heard.json'))
VOFF=0.5; SHIFT=0.2
# silences in voice
out=subprocess.run(['ffmpeg','-i','aud/vo16.wav','-af','silencedetect=noise=-38dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',out)]; se=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',out)]
sil=list(zip(ss,se))
T=[]
for w,t in W:
    t2=t+SHIFT
    for a,b in sil:
        if a-0.05<=t2<b:
            t2 = b if t2>=(a+b)/2 else t
    T.append(round(t2,3))
# fix monotonic
for i in range(1,len(T)):
    if T[i]<=T[i-1]: T[i]=round(T[i-1]+0.06,3)
# chunks: list of [ (display, ntokens, key) ]
C=[
 [("Three",1,1),("things",1),("every",1),("trader",1)],
 [("should",1),("know",1),("before",1)],
 [("Wednesday's",1),("PCE.",3,1)],
 [("One:",1,1)],
 [("it's",1),("the",1),("Fed's",1),("favourite",1)],
 [("inflation",1,1),("gauge.",1)],
 [("The",1),("target",1),("is",1),("2%,",3,1)],
 [("and",1),("October's",1),("headline",1)],
 [("is",1),("expected",1),("near",1),("3.8%.",5,1)],
 [("Two:",1,1)],
 [("the",1),("surprise",1,1),("is",1),("what",1),("moves",1),("markets.",1)],
 [("Core",1),("is",1),("forecast",1),("to",1),("rise",1)],
 [("0.3%",4,1),("for",1),("the",1),("month.",1)],
 [("Hotter",1,1),("can",1),("mean",1),("rate",1),("worries.",1)],
 [("Softer",1,1),("can",1),("mean",1),("relief.",1)],
 [("Three:",1,1)],
 [("it",1),("drops",1),("at",1),("8:30",2,1),("Eastern,",1)],
 [("with",1),("GDP,",2)],
 [("the",1),("day",1),("before",1),("Thanksgiving.",1)],
 [("The",1),("Nasdaq",1),("fell",1),("5.6%",5,1),("on",1),("Friday,",1)],
 [("then",1),("ripped",1,1),("higher",1),("on",1),("Monday,",1)],
 [("so",1),("know",1),("your",1),("risk",1,1)],
 [("before",1),("the",1),("number",1),("lands.",1)],
 [("Are",1),("you",1),("trading",1),("the",1),("release,",1)],
 [("or",1),("waiting",1),("it",1),("out?",1)],
]
k=0; chunks=[]
for ch in C:
    ws=[]
    for it in ch:
        d,n=it[0],it[1]; key=len(it)>2
        ws.append({'t':d,'s':round(T[k]+VOFF,3),'k':key}); k+=n
    chunks.append({'w':ws,'s':ws[0]['s']})
assert k==len(T),(k,len(T))
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','aud/vo16.wav'],capture_output=True,text=True).stdout)
for i,c in enumerate(chunks):
    c['e']=round(chunks[i+1]['s']-0.04,3) if i+1<len(chunks) else round(dur+VOFF+0.35,3)
tok=[T[i]+VOFF for i in range(len(T))]
json.dump({'chunks':chunks,'tok':tok,'VOFF':VOFF,'VEND':round(dur+VOFF,3)},open('tl.json','w'),indent=1)
open('tl.js','w').write('const TL='+json.dumps({'chunks':chunks,'tok':tok,'VOFF':VOFF,'VEND':round(dur+VOFF,3)})+';\n')
for c in chunks: print(c['s'],c['e'],' '.join(f"{w['t']}@{w['s']}" for w in c['w']))
