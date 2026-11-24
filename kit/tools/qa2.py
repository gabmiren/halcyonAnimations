import subprocess,sys,os
from PIL import Image,ImageDraw,ImageFont
V=sys.argv[1]; Q=sys.argv[2]; os.makedirs(Q+'/all',exist_ok=True); os.makedirs(Q+'/sheets',exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',V,'-q:v','3','-start_number','0',f'{Q}/all/%05d.jpg'],check=True)
SC=[('hook',0,124),('ch1_gauge',125,365),('ch2_register',366,645),('ch3_flaps',646,792),('ch3_recorder',793,1082),('off',1083,1094),('end',1095,1157)]
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',44)
def lab(Fn,name):
    im=Image.open(f'{Q}/all/{Fn:05d}.jpg').convert('RGB');d=ImageDraw.Draw(im);d.rectangle([60,250,940,1470],outline=(255,0,0),width=3);d.rectangle([10,10,420,70],fill=(0,0,0));d.text((20,16),f'{name} f{Fn}',font=F,fill=(255,255,255));return im
def tile(ims,w,out,pad=10):
    ims=[i.resize((w,int(w*16/9))) for i in ims];s=Image.new('RGB',(len(ims)*(w+pad),ims[0].height),(34,34,34))
    for k,i in enumerate(ims): s.paste(i,(k*(w+pad),0))
    s.save(out)
for nm,a,b in SC:
    fs=sorted(set([a,min(b,a+3),(a+b)//2,max(a,b-3),b])); tile([lab(f,nm) for f in fs],360,f'{Q}/sheets/{nm}.png')
for i,(_,c,_) in enumerate(SC[1:]):
    tile([lab(f,f'c{i}') for f in range(c-5,c+5)],216,f'{Q}/sheets/cut{i}_strip.png',6)
print('ok')
