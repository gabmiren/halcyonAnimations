import sys, numpy as np, soundfile as sf, librosa, pyloudnorm as pl, scipy.signal as ss
sys.path.insert(0,'/home/claude/pcedata'); from variants import V
n=sys.argv[1]; c=V[n]; sr=48000; M=pl.Meter(sr); NV='/home/claude/nvearn/'
DUR=c['end']; N=int(round(DUR*sr)); rng=np.random.default_rng(7)
load=lambda f: librosa.load(f,sr=sr,mono=True)[0].astype(np.float32)
mu=load(c.get('music',f'aud/music_{n}.wav')); mu=np.pad(mu,(0,max(0,N-len(mu))))[:N]
mu*=10**((-20-M.integrated_loudness(mu.astype(np.float64)))/20)
sfx=np.zeros(N,np.float32); LOG=[]
def rms(x): return float(np.sqrt((x.astype(np.float64)**2).mean())+1e-9)
def rms_peak(x): w2=int(.12*sr); return np.sqrt(np.convolve(x**2,np.ones(w2)/w2,'same')).max()+1e-9
def put(x,at,rel,align_peak=False,name=''):
    x=x/rms_peak(x); pk=np.argmax(np.abs(x))/sr if align_peak else 0; o=int((at-pk)*sr)
    a=max(0,int(at*sr)); ref=max(rms(mu[a:a+int(.12*sr)]),10**(-38/20)); y=x*ref*10**(rel/20)
    if o<0: y=y[-o:]; o=0
    m=min(len(y),N-o)
    if m>0: sfx[o:o+m]+=y[:m]
    if name: LOG.append((name,at))
def env_ad(m,a,d): k=np.arange(m); return np.minimum(1,k/max(1,a*sr))*np.exp(-k/(d*sr))
def static(d):
    m=int(d*sr); x=rng.standard_normal(m).astype(np.float32); b,a=ss.butter(2,[700/(sr/2),9000/(sr/2)],'band'); x=ss.lfilter(b,a,x).astype(np.float32)
    e=np.minimum(1,np.arange(m)/(.005*sr))*np.minimum(1,(m-np.arange(m))/(.06*sr)); return x*e
def blip(freq,d=0.045,sq=True):
    m=int(d*sr); k=np.arange(m)/sr; x=np.sign(np.sin(2*np.pi*freq*k)) if sq else np.sin(2*np.pi*freq*k)
    b,a=ss.butter(2,5000/(sr/2)); x=ss.lfilter(b,a,x); return (x*env_ad(m,0.002,d/3)).astype(np.float32)
def swish(d=0.25,f0=900,f1=300):
    m_=int(d*sr); k=np.arange(m_)/sr; fq=np.linspace(f0,f1,m_); ph=2*np.pi*np.cumsum(fq)/sr
    x=rng.standard_normal(m_)*0.5+np.sin(ph)*0.4; b_,a_=ss.butter(2,[300/(sr/2),4000/(sr/2)],'band'); x=ss.lfilter(b_,a_,x)
    return (x*np.sin(np.pi*k/d)).astype(np.float32)
thud=load(NV+'sfx/thud.wav'); b,a=ss.butter(2,1400/(sr/2)); thud=ss.lfilter(b,a,thud).astype(np.float32)
H=c['hits']; D=c['drop']; B2=c['b2']; B3=c['b3']
put(static(0.12),0.0,-12)
for i,h in enumerate(H):
    put(blip([1100,1300,1550,1900][i],0.07,False),h,-4,name=f'bar{i+1}')
    for k in range(5): put(blip(2400,0.012,True),h+0.04+k*0.06,-15)
put(thud,D+0.01,-5,True,name='drop'); put(static(0.09),D,-13); put(swish(0.45,700,1500),D+0.05,-15)
put(thud,D+0.2,-7,True,name='stamp')
put(blip(2200,0.08,False),B2+0.08,-6,name='b2'); 
if c.get('k2',1) is not None: put(blip(2600,0.06,False),B2+0.46,-7)
put(swish(0.3,1100,300),B3-0.08,-14); put(thud,B3+0.02,-7,True,name='end')
sf.write(f'aud/mix_pre.wav',mu+sfx,sr); sf.write(f'aud/st_mu_{n}.wav',mu,sr); sf.write(f'aud/st_sfx_{n}.wav',sfx,sr)
def db(x): return 20*np.log10(rms(x))
print(n,' '.join(f"{nm}:{db(sfx[int(t*sr):int((t+.12)*sr)])-db(mu[int(t*sr):int((t+.12)*sr)]):+.1f}" for nm,t in LOG))
