#!/bin/bash
set -e

if [ "$#" -lt 1 ]; then
    echo "Usage: $(basename $0) [channel] [date?]"
    exit 1
fi

CHANNEL=$1
DATE=$2

cd $(dirname ${BASH_SOURCE[0]})

filename_title=$(python plot.py $DATE)
echo \$filename_title = "$filename_title"
filename=$(echo "$filename_title" | sed -n 1p)
title=$(echo "$filename_title" | sed -n 2p)

python send.py $CHANNEL $filename "$title"
