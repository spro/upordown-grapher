#!/bin/bash
set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $(basename $0) [channel] [title]"
fi

CHANNEL=$1
TITLE=$2
echo \$CHANNEL = $CHANNEL
echo \$TITLE = $TITLE
exit

filename=$(python plot.py)
echo \$filename = $filename
coffee ../upordown-mention/test-send-image.coffee $CHANNEL $filename $TITLE
