import numpy as np, soundfile as sf, json, librosa, pyloudnorm as pl, scipy.signal as ss, sys
import os
D=os.getcwd()+'/'; LIB=os.environ.get('HALCYON_LIB',os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))+'/'; sr=48000; M=pl.Meter(sr)
TL=json.load(open(D+'tl.json')); VOFF=TL['VOFF']; DUR=38.6; N=int(round(DUR*sr)); t=np.arange(N)/sr
S=dict(c1=4.15,c2=12.2,c3=21.55,c4=26.45,off=36.1,end=36.5)
OUT=sys.argv[1] if len(sys.argv)>1 else 'aud/mix_pre.wav'
load=lambda f: librosa.load(f,sr=sr,mono=True)[0].astype(np.float32)
rng=np.random.default_rng(11)
# voice
v=load(D+'aud/vo48.wav'); f=int(.08*sr); v[:f]*=np.linspace(0,1,f)
vo=np.zeros(N,np.float32); o=int(VOFF*sr); n=min(len(v),N-o); vo[o:o+n]=v[:n]
Lv=M.integrated_loudness(vo.astype(np.float64)); vo*=10**((-20-Lv)/20)
# music
mu=load(LIB+'audio/music/music_starlight.mp3'); mu=np.pad(mu,(0,max(0,N-len(mu))))[:N]
Lm=M.integrated_loudness(mu[:int(30*sr)].astype(np.float64))
g=10**(((-20-12.5)-Lm)/20); env=np.full(N,g,np.float32)
w=int(.02*sr); fr=np.sqrt((vo[:N//w*w].reshape(-1,w)**2).mean(1)); act=(fr>fr.max()*0.03).astype(np.float32)
act=np.convolve(np.convolve(act,np.ones(11),'same')>0,np.ones(20)/20,'same'); act=np.pad(np.repeat(act,w),(0,N))[:N]
env*=10**(-2*act/20)
env*=10**(3.5*np.clip((t-S['end'])/0.4,0,1)/20)
env*=np.minimum(1,t/0.05); env*=np.clip((DUR-t)/2.0,0,1)**1.5
# slight "tape" wobble on the music for the 90s feel
wob=1+0.0025*np.sin(2*np.pi*0.6*t)
idx=np.clip(np.cumsum(wob)-wob[0],0,N-1); mu=np.interp(idx,np.arange(N),mu).astype(np.float32)
music=mu*env
# reference voice rms
va=vo[o:o+n]; f2=np.sqrt((va[:len(va)//w*w].reshape(-1,w)**2).mean(1)); VR=float(np.sqrt((f2[f2>f2.max()*0.1]**2).mean()))
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
thud=load(LIB+'audio/sfx/thud.wav'); b,a=ss.butter(2,1400/(sr/2)); thud=ss.lfilter(b,a,thud).astype(np.float32)
sw=load(LIB+'audio/sfx/swoosh.mp3'); click=load(LIB+'audio/sfx/click.mp3')
W=[w for c in TL['chunks'] for w in c['w']]
def ws(txt,after=0): return [x['s'] for x in W if x['t']==txt and x['s']>after][0]
# static bursts on cuts
for c in [S['c1'],S['c2'],S['c3'],S['c4']]: put(static(0.16),c,-18)
# hook
put(thud,0.02,-13,True); put(thud,ws('PCE.'),-17,True)
def swish(d=0.25,f0=900,f1=300):
    m_=int(d*sr); k=np.arange(m_)/sr; fq=np.linspace(f0,f1,m_); ph=2*np.pi*np.cumsum(fq)/sr
    x=rng.standard_normal(m_)*0.5+np.sin(ph)*0.4; b_,a_=ss.butter(2,[300/(sr/2),4000/(sr/2)],'band'); x=ss.lfilter(b_,a_,x)
    return (x*np.sin(np.pi*k/d)).astype(np.float32)
put(blip(1300,0.05,False),ws('inflation'),-17)
put(swish(0.3),8.1,-24); put(thud,ws('2%,'),-17,True)
put(swish(0.45,1100,250),10.78,-22); put(thud,ws('3.8%.'),-14,True)
def beep(f=2200,d=0.09): return blip(f,d,False)
put(beep(2600,0.07),13.22,-12); put(beep(2600,0.07),13.42,-12)
put(beep(2200),ws('0.3%'),-17); put(thud,ws('0.3%'),-19,True)
for k in range(3): put(beep(1800,0.05),17.9+k*0.33,-17)
put(beep(2800,0.08),ws('Hotter'),-12); put(beep(1400,0.1),ws('Softer'),-12)
def clack():
    m_=int(0.018*sr); x=rng.standard_normal(m_); b_,a_=ss.butter(2,[1500/(sr/2),8000/(sr/2)],'band'); x=ss.lfilter(b_,a_,x)
    return (x*np.exp(-np.arange(m_)/(0.004*sr))).astype(np.float32)
for t0 in [22.5,23.2,24.68,25.2]:
    for k in range(18): put(clack(),t0+k*0.03+rng.uniform(0,0.01),-17)
put(thud,ws('8:30'),-19,True)
def scratch(d):
    m_=int(d*sr); x=rng.standard_normal(m_); b_,a_=ss.butter(2,[2500/(sr/2),9000/(sr/2)],'band'); x=ss.lfilter(b_,a_,x)
    e=0.6+0.4*np.sin(np.arange(m_)/sr*2*np.pi*13); return (x*e*np.minimum(1,np.arange(m_)/(0.05*sr))*np.minimum(1,(m_-np.arange(m_))/(0.08*sr))).astype(np.float32)
put(scratch(0.9),27.3,-30); put(thud,ws('5.6%'),-15,True)
put(scratch(0.95),29.55,-30); put(thud,ws('ripped'),-17,True)
put(thud,31.6,-12,True); put(static(0.06),31.6,-26)
put(crt_off(),S['off'],-13)
put(thud,S['end']+0.02,-17,True)
# tape hiss bed under footage scenes
h=rng.standard_normal(N).astype(np.float32); b,a=ss.butter(2,[3000/(sr/2),12000/(sr/2)],'band'); h=ss.lfilter(b,a,h).astype(np.float32)
he=np.where(t<S['off'],1,0).astype(np.float32); h*=he; h=h/np.sqrt((h**2).mean()+1e-9)*VR*10**(-44/20)
mix=vo+music+sfx+h
sf.write(D+OUT,mix,sr)
print('voice',round(Lv,1),'music dB',round(20*np.log10(g),1),'peak',round(float(np.abs(mix).max()),2))
