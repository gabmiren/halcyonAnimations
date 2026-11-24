#!/usr/bin/env bash
# Rebuilds fr/ (graded frames) from the library so page.html renders.
set -e; LIB=$(cd "$(dirname "$0")/../.." && pwd); G=$LIB/kit/tools/grade.sh; cd "$(dirname "$0")"; mkdir -p fr
$G hook $LIB/footage/ai/ant90_pit.mp4 fr/pit
$G hook $LIB/footage/ai/ant90_street.mp4 fr/street
$G still $LIB/images/ai/ant90_pit.png fr/pit_blur.jpg
cp $LIB/images/ai/ant90_desk.png fr/ant90_desk.png
