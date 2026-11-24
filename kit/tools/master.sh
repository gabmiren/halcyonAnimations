set -e; V="$1"; OUT="$2"   # run from the reel folder; needs aud/mix_pre.wav from mix.py
ffmpeg -nostdin -v error -y -i aud/mix_pre.wav -af "alimiter=limit=0.38:attack=2:release=80:level=disabled" aud/mix_lim.wav
J=$(ffmpeg -nostdin -hide_banner -i aud/mix_lim.wav -af loudnorm=I=-13.3:TP=-2.4:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
set -- "$V" "$OUT" $(echo "$J"|python3 -I -c "import json,sys;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
ffmpeg -nostdin -v error -y -i aud/mix_lim.wav -af "loudnorm=I=-13.3:TP=-2.4:LRA=11:measured_I=$3:measured_TP=$4:measured_LRA=$5:measured_thresh=$6:offset=$7:linear=true,aresample=48000" aud/mix.wav
ffmpeg -nostdin -v error -y -i "$1" -i aud/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$2"
ffmpeg -nostdin -hide_banner -i "$2" -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +I:|Peak:"
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 "$2"
