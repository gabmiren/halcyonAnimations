#!/usr/bin/env bash
# 90s VHS grade for any clip or still. Output is a 1080x1920 JPG frame sequence the reel pages read.
#   grade.sh hook  <in.mp4> <outdir>      sharp foreground footage (24 fps, grain, chroma bleed, vignette)
#   grade.sh blur  <in.mp4> <outdir>      soft dark background plate (12 fps)
#   grade.sh still <in.png> <out.jpg>     blurred dark backdrop from a still
set -e; MODE=$1; IN=$2; OUT=$3
COVER="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
case $MODE in
 hook) mkdir -p "$OUT"; ffmpeg -v error -y -i "$IN" -vf "fps=24,$COVER,gblur=sigma=1.0,eq=saturation=0.8:contrast=1.06:brightness=-0.02,rgbashift=rh=-4:bh=4,noise=alls=9:allf=t,vignette=PI/4.5" -q:v 3 "$OUT/%03d.jpg";;
 blur) mkdir -p "$OUT"; ffmpeg -v error -y -i "$IN" -vf "fps=12,scale=540:960:force_original_aspect_ratio=increase,crop=540:960,gblur=sigma=9,eq=saturation=0.6:brightness=-0.18,scale=1080:1920" -q:v 4 "$OUT/%03d.jpg";;
 still) ffmpeg -v error -y -i "$IN" -vf "$COVER,gblur=sigma=22,eq=brightness=-0.3:saturation=0.8" -q:v 3 "$OUT";;
 *) echo "mode: hook | blur | still"; exit 1;;
esac
echo "graded $IN -> $OUT"
