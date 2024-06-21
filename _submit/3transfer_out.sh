#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
IP=34.140.239.112
(cd $SCRIPTPATH/../ &&  rsync -azv --stats -P  --exclude='**/__pycache__' --exclude='**/*.pt' --exclude='**/*.png' --exclude='.venv' --exclude='**/cifar*' --exclude='**/*.log' $IP:~/decentralizepy/eval/data/ ./.saved_experiments && cd _submit)
