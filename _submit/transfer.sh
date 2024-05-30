#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
(cd $SCRIPTPATH/../ &&  rsync -azv -e 'ssh -A -J sdeheredia@student-linux.tudelft.nl' --exclude='eval/' --exclude='**/decentralizepy.egg-info' --exclude='**/__pycache__' --exclude='.venv' [!.]* sdeheredia@login.delftblue.tudelft.nl:/scratch/sdeheredia/decentralizepy && cd _submit)
