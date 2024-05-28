#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
(cd $SCRIPTPATH/../ &&  rsync -azv -e 'ssh -A -J sdeheredia@student-linux.tudelft.nl' --exclude='**/__pycache__' --exclude='.venv' [!.]* sdeheredia@login.delftblue.tudelft.nl:./decentralizepy && cd _submit)
