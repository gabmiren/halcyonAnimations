import sherpa_onnx, numpy as np, json, re, subprocess, difflib, soundfile as sf, sys
V=sys.argv[1]
d="/home/claude/models/sherpa-onnx-whisper-small.en/"
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+"small.en-encoder.int8.onnx",decoder=d+"small.en-decoder.int8.onnx",tokens=d+"small.en-tokens.txt",num_threads=2)
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',V,'-ac','1','-ar','16000','aud/r16.wav'],check=True)
a,sr=sf.read('aud/r16.wav',dtype='float32')
SENT=[("three things every trader should know before wednesdays pce",0.5,4.0),("one its the feds favourite inflation gauge the target is two percent and octobers headline is expected near three point eight percent",4.2,12.0),
("two the surprise is what moves markets core is forecast to rise point three percent for the month hotter can mean rate worries softer can mean relief",12.2,21.4),
("three it drops at eight thirty eastern with gdp the day before thanksgiving",21.6,26.4),("the nasdaq fell five point six percent on friday then ripped higher on monday so know your risk before the number lands",26.5,33.1),("are you trading the release or waiting it out",33.1,36.0)]
NORM=[(r'\b100\b','one hundred'),(r'\b17\b','seventeen'),(r'\b2\b','two'),(r'1,?500','fifteen hundred'),(r'\b0?\.3\b','point three'),(r'\b3\.8\b','three point eight'),(r'\b8 ?:? ?30\b','eight thirty'),(r'\b830\b','eight thirty'),(r'\bp\.?c\.?e\.?\b','pce'),(r'g\.?d\.?p\.?','gdp'),(r'favorite','favourite'),(r'\bwednesday s\b','wednesdays'),(r'\bfed s\b','feds'),(r'\boctober s\b','octobers'),(r'\b1\b','one'),(r'\b2\b','two'),(r'\b3\b','three'),(r'\b5\.6','five point six'),(r'\b30\b','thirty'),(r'\b6\b','six'),(r'\b50k\b','fifty k'),(r'\$50k','fifty k'),(r'ceo','ceo'),(r'c\.?e\.?o\.?','ceo'),(r'\b1,500\b','fifteen hundred'),(r'\bnvidia s\b','nvidias'),(r'%',' percent'),(r'per cent','percent'),(r'n\.?q\.?\b','nq'),(r'n q\b','nq'),(r'a\.?i\.?\b','ai'),(r'draw down','drawdown'),(r'a hundred','one hundred'),(r"that's",'thats'),(r"nvidia's",'nvidias'),(r'jensen hwang|jensen wong|jenson huang','jensen huang'),(r'\b100\b','one hundred'),(r'one hundred points','a hundred points'),(r'cues','queues'),(r'vander|vandah|vonda|wanda','vanda')]
def norm(x):
    x=x.lower()
    for p,q in NORM: x=re.sub(p,q,x)
    return re.sub(r'[^a-z ]',' ',x).split()
bad=0
for ex,s,e in SENT:
    seg=a[int(s*sr):int(e*sr)]; st=r.create_stream(); st.accept_waveform(sr,seg); r.decode_stream(st); h=st.result.text.strip()
    E=norm(ex);H=norm(h);ops=[o for o in difflib.SequenceMatcher(None,E,H).get_opcodes() if o[0]!='equal']
    iss=[(o[0],' '.join(E[o[1]:o[2]]),' '.join(H[o[3]:o[4]])) for o in ops]; bad+=len(iss)
    print('OK  ' if not iss else 'DIFF',h,iss if iss else '')
print('diffs',bad)
