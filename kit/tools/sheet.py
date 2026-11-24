import sys,glob
from PIL import Image
d=sys.argv[1];n=int(sys.argv[2]) if len(sys.argv)>2 else 9
fs=sorted(glob.glob(d+'/*.jpg'));ims=[Image.open(f).resize((270,480)) for f in fs]
for k in range(0,len(ims),n):
  s=Image.new('RGB',(n*276,486),(40,40,40))
  for i,im in enumerate(ims[k:k+n]): s.paste(im,(i*276,3))
  s.save(f'{d}/sheet{k//n}.png')
print(len(fs))
