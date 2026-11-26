import numpy as np, soundfile as sf, librosa, pyloudnorm as pl, scipy.signal as ss, sys
D='/home/claude/pcedata/'; NV='/home/claude/nvearn/'; sr=48000; M=pl.Meter(sr)
DUR=14.0; N=int(DUR*sr); t=np.arange(N)/sr
load=lambda f: librosa.load(f,sr=sr,mono=True)[0].astype(np.float32)
rng=np.random.default_rng(7)
mu=load(D+'aud/music.wav'); mu=np.pad(mu,(0,max(0,N-len(mu))))[:N]
Lm=M.integrated_loudness(mu.astype(np.float64)); mu*=10**((-20-Lm)/20)
w=int(.02*sr); f2=np.sqrt((mu[:N//w*w].reshape(-1,w)**2).mean(1)); VR=float(np.sqrt((f2[f2>f2.max()*0.1]**2).mean()))
sfx=np.zeros(N,np.float32)
def rms_peak(x): w2=int(.12*sr); return np.sqrt(np.convolve(x**2,np.ones(w2)/w2,'same')).max()+1e-9
sfx=np.zeros(N,np.float32)
def put(x,at,db,align_peak=False):
    y=x/rms_peak(x)*VR*10**(db/20); pk=np.argmax(np.abs(y))/sr if align_peak else 0
    o2=int((at-pk)*sr)
    if o2<0: y=y[-o2:]; o2=0
    m=min(len(y),N-o2)
    if m>0: sfx[o2:o2+m]+=y[:m]
def env_ad(m,a,d): k=np.arange(m); return np.minimum(1,k/max(1,a*sr))*np.exp(-k/(d*sr))
def static(d):
    m=int(d*sr); x=rng.standard_normal(m).astype(np.float32)
    b,a=ss.butter(2,[700/(sr/2),9000/(sr/2)],'band'); x=ss.lfilter(b,a,x).astype(np.float32)
    cr=(rng.random(m)<0.002).astype(np.float32)*rng.uniform(2,5,m); x=x+cr
    e=np.minimum(1,np.arange(m)/(.005*sr))*np.minimum(1,(m-np.arange(m))/(.06*sr)); return x*e
def blip(freq,d=0.045,sq=True):
    m=int(d*sr); k=np.arange(m)/sr; x=np.sign(np.sin(2*np.pi*freq*k)) if sq else np.sin(2*np.pi*freq*k)
    b,a=ss.butter(2,5000/(sr/2)); x=ss.lfilter(b,a,x)
    return (x*env_ad(m,0.002,d/3)).astype(np.float32)
def chime():
    m=int(0.5*sr); k=np.arange(m)/sr; x=np.zeros(m)
    for fq,st,amp in [(659.3,0,1),(987.8,0.09,0.9),(1318.5,0.18,0.6)]:
        s0=int(st*sr); kk=k[:m-s0]; x[s0:]+=amp*np.sin(2*np.pi*fq*kk)*np.exp(-kk/0.22)*np.minimum(1,kk/0.004)
    return x.astype(np.float32)
def crt_off():
    m=int(0.55*sr); k=np.arange(m)/sr
    fq=110*np.exp(-k/0.12)+38; ph=2*np.cumsum(np.pi*fq/sr); low=np.sin(ph)*np.exp(-k/0.18)
    hi=np.sin(2*np.pi*7800*k)*np.exp(-k/0.12)*0.05
    zap=static(0.07); z=np.zeros(m); z[:len(zap)]=zap*0.5
    return (low+hi+z).astype(np.float32)
thud=load(NV+'sfx/thud.wav'); b,a=ss.butter(2,1400/(sr/2)); thud=ss.lfilter(b,a,thud).astype(np.float32)
def swish(d=0.25,f0=900,f1=300):
    m_=int(d*sr); k=np.arange(m_)/sr; fq=np.linspace(f0,f1,m_); ph=2*np.pi*np.cumsum(fq)/sr
    x=rng.standard_normal(m_)*0.5+np.sin(ph)*0.4; b_,a_=ss.butter(2,[300/(sr/2),4000/(sr/2)],'band'); x=ss.lfilter(b_,a_,x)
    return (x*np.sin(np.pi*k/d)).astype(np.float32)
HITS=[1.32,2.72,4.09,5.46]; DROP=6.13; B2=8.92; B3=11.70
put(static(0.12),0.0,-24)
for i,h in enumerate(HITS):
    put(blip([1100,1300,1550,1900][i],0.07,False),h,[-13,-13,-13,-17][i])
    for k in range(5): put(blip(2400,0.012,True),h+0.04+k*0.06,-24)
put(thud,DROP+0.01,-4,True); put(static(0.09),DROP,-19)
put(swish(0.45,700,1500),DROP+0.05,-23)
put(thud,DROP+0.2,-7,True)
put(blip(2200,0.08,False),B2+0.08,-6); put(blip(2600,0.06,False),B2+0.46,-6)
put(swish(0.3,1100,300),B3-0.08,-21); put(thud,B3+0.02,-6,True)
mix=mu+sfx
sf.write(D+'aud/mix_pre.wav',mix,sr); sf.write(D+'aud/st_mu.wav',mu,sr); sf.write(D+'aud/st_sfx.wav',sfx,sr)
print('ok',M.integrated_loudness(mix.astype(np.float64)))
