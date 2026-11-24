import numpy as np, soundfile as sf, json, librosa, pyloudnorm as pl, scipy.signal as ss, sys
import os
D=os.getcwd()+'/'; LIB=os.environ.get('HALCYON_LIB',os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))+'/'; sr=48000; M=pl.Meter(sr)
TL=json.load(open(D+'tl.json')); VOFF=TL['VOFF']; DUR=36.9; N=int(round(DUR*sr)); t=np.arange(N)/sr
S=dict(board=5.15,win=9.45,desk=17.15,dd=25.75,off=34.4,end=34.8)
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
for c in [S['board'],S['win'],S['desk']]: put(static(0.16),c,-18)
put(static(0.1),S['dd'],-23)
# hook lands
put(thud,ws('back'),-17,True)
put(thud,ws('surging.'),-16,True)
# LED board
put(thud,ws('reinstated'),-18,True)
for k in range(9): put(blip(1900,0.03),7.8+k*0.04,-30)
put(thud,ws('30%'),-14,True)
# window
put(chime(),S['win']+0.28,-24)
put(click,10.68,-24,True)
put(sw,13.14,-22); put(thud,ws('rips,'),-17,True)
put(thud,14.0,-19,True)
for k in range(17): put(blip(700+k*45,0.035),15.25+k*0.066,-31)
put(thud,ws('6%.'),-16,True)
# chart
put(blip(700,0.08,False),19.0,-28); put(thud,ws('5.6%.'),-15,True)
put(blip(1300,0.05,False),21.45,-30)
put(blip(1100,0.08,False),23.15,-28); put(thud,ws('1,500',23),-16,True)
put(blip(1500,0.06,False),24.9,-30)
# drawdown
put(blip(1200,0.05,False),26.2,-30)
put(thud,ws('100'),-16,True)
for k in range(6): put(blip(1000+(k%2)*300,0.04),30.95+k*0.17,-31)
put(click,32.18,-25,True); put(thud,32.65,-19,True)
put(crt_off(),S['off'],-13)
put(thud,S['end']+0.02,-17,True)
# tape hiss bed under footage scenes
h=rng.standard_normal(N).astype(np.float32); b,a=ss.butter(2,[3000/(sr/2),12000/(sr/2)],'band'); h=ss.lfilter(b,a,h).astype(np.float32)
he=np.where(t<S['off'],1,0).astype(np.float32); h*=he; h=h/np.sqrt((h**2).mean()+1e-9)*VR*10**(-44/20)
mix=vo+music+sfx+h
sf.write(D+OUT,mix,sr)
print('voice',round(Lv,1),'music dB',round(20*np.log10(g),1),'peak',round(float(np.abs(mix).max()),2))
