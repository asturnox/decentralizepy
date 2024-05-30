#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
(cd $SCRIPTPATH/../ &&  rsync -azv --progress --stats --exclude='**/2024*' --exclude='**/decentralizepy.egg-info' --exclude='**/__pycache__' --exclude='.venv' [!.]* 35.195.100.250:~/decentralizepy && cd _submit)
