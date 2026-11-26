set -e; cd /home/claude/pcedata; n="$1"; ver="${2:-v1}"
python3 -I -c "
import sys,json;sys.path.insert(0,'.');from variants import V
c={k:v for k,v in V['$n'].items() if k in('hits','drop','b2','b3','end','k2','send')}
s=open('pced_tpl.html').read().replace('/*CFG*/','window.CFG='+json.dumps(c)+';');open('pce_$n.html','w').write(s)"
python3 -I prep_music.py $n
python3 -I mix_var.py $n
E=$(python3 -I -c "import sys;sys.path.insert(0,'.');from variants import V;print(V['$n']['end'])")
bash go.sh pce_$n.html $E 6
bash master.sh pce_$n.mp4 halcyon_pce_data_${n}_$ver.mp4
D=$(python3 -I -c "import sys;sys.path.insert(0,'.');from variants import V;print(V['$n']['drop']+0.77)")
node snap.js pce_$n.html cov_$n $D >/dev/null && cp cov_$n/*.jpg halcyon_pce_data_${n}_cover_$ver.jpg
