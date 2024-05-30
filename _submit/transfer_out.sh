#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
(cd $SCRIPTPATH/../ &&  rsync -azv --stats -P -e 'ssh -A -J sdeheredia@student-linux.tudelft.nl'  --exclude='**/__pycache__' --exclude='.venv' --exclude='**/cifar*' --exclude='**/*.log' 35.195.100.250:~/decentralizepy/eval/data/ ./.saved_experiments && cd _submit)
