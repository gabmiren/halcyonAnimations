#!/usr/bin/env bash
# Needs the two Pexels clips in footage/stock/ first (see footage/stock/SOURCES.md).
set -e; LIB=$(cd "$(dirname "$0")/../.." && pwd); G=$LIB/kit/tools/grade.sh; cd "$(dirname "$0")"; mkdir -p fr
$G hook $LIB/footage/stock/pexels_29376327_aisle.mp4 fr/aisle
$G blur $LIB/footage/stock/pexels_29376327_aisle.mp4 fr/aisleb
$G blur $LIB/footage/stock/pexels_29068393_cart.mp4 fr/cartb
