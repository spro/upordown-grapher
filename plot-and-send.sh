#!/bin/bash
set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $(basename $0) [channel] [title] [date?]"
    exit 1
fi

CHANNEL=$1
TITLE=$2
DATE=$3

cd $(dirname ${BASH_SOURCE[0]})

filename=$(python plot.py $DATE)
echo \$filename = $filename
python send.py $CHANNEL $filename "$TITLE"
