#!/usr/bin/env bash
set -e; LIB=$(cd "$(dirname "$0")/../.." && pwd); G=$LIB/kit/tools/grade.sh; cd "$(dirname "$0")"; mkdir -p fr
$G hook $LIB/footage/ai/nvh_chip.mp4 fr/chip
$G hook $LIB/footage/ai/nvh_room.mp4 fr/room
$G still $LIB/images/ai/ant90_pit.png fr/pit_blur.jpg
cp $LIB/images/ai/ant90_desk.png fr/ant90_desk.png
