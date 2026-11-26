import sys, numpy as np, soundfile as sf, librosa, scipy.signal as ss
sys.path.insert(0,'/home/claude/pcedata'); from variants import V
n=sys.argv[1]; c=V[n]; sr=48000
if 'music' in c and n=='runaway': sys.exit(0)
y,_=librosa.load('assets/'+c['src'],sr=sr,mono=True)
N=int(c['end']*sr); a=int(c['start']*sr); seg=y[a:a+N].astype(np.float64)
if c.get('tail'):
    L=len(seg); rng=np.random.default_rng(3); ir=rng.standard_normal(int(1.4*sr))*np.exp(-np.arange(int(1.4*sr))/(0.35*sr))
    b,a2=ss.butter(2,4000/(sr/2)); ir=ss.lfilter(b,a2,ir); ir/=np.sqrt((ir**2).sum())
    last=seg[-int(0.5*sr):]*np.linspace(0,1,int(0.5*sr)); wet=ss.fftconvolve(last,ir)[int(0.5*sr):]
    tail=np.zeros(N-L); m=min(len(tail),len(wet)); tail[:m]=wet[:m]*0.9
    xf=int(0.012*sr); seg=np.concatenate([seg,tail]); seg[L-xf:L]*=np.linspace(1,0.85,xf)
seg=np.pad(seg,(0,max(0,N-len(seg))))[:N]
fi=int(0.03*sr); seg[:fi]*=np.linspace(0,1,fi)
fo=int(1.6*sr); seg[-fo:]*=np.linspace(1,0,fo)**1.6
sf.write(f'aud/music_{n}.wav',seg.astype(np.float32),sr); print(n,len(seg)/sr)
