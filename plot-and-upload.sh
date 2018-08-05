#!/bin/bash
set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $(basename $0) [channel] [title] [date?]"
fi

CHANNEL=$1
TITLE=$2
DATE=$3

filename=$(python plot.py $DATE)
echo \$filename = $filename
coffee ../upordown-mention/test-send-image.coffee $CHANNEL $filename $TITLE
