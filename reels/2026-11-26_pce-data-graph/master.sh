set -e; cd /home/claude/pcedata; V="$1"; OUT="$2"
meas(){ ffmpeg -nostdin -hide_banner -i "$1" -af ebur128=peak=true -f null - 2>&1 | awk '/^ +I:/{i=$2} /^ +Peak:/{p=$2} END{print i, p}'; }
ffmpeg -nostdin -v error -y -i aud/mix_pre.wav -af "volume=5.4dB,alimiter=limit=0.35:attack=1:release=60:level=disabled,aresample=48000" aud/mix_lim.wav
read I P <<<"$(meas aud/mix_lim.wav)"
G=$(python3 -I -c "print(round(min(-14.0-($I),-3.4-($P)),2))")
ffmpeg -nostdin -v error -y -i aud/mix_lim.wav -af "volume=${G}dB" aud/mix.wav
ffmpeg -nostdin -v error -y -i "$V" -i aud/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
echo "gain $G -> $(meas "$OUT")"
