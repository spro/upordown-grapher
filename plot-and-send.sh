#!/bin/bash
set -e

if [ "$#" -lt 1 ]; then
    echo "Usage: $(basename $0) [channel] [date?]"
    exit 1
fi

CHANNEL=$1
DATE=$2

cd $(dirname ${BASH_SOURCE[0]})

python send.py $CHANNEL $(python plot.py $DATE)
