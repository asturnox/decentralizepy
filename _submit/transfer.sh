#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
IP=35.233.110.168
(cd $SCRIPTPATH/../ &&  rsync -azv --progress --stats --exclude='tutorial/dynamic*' --exclude='**/2024*' --exclude='**/decentralizepy.egg-info' --exclude='**/__pycache__' --exclude='.venv' [!.]* $IP:~/decentralizepy && cd _submit)
