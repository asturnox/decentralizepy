#!/bin/bash

cd ../

cd tutorial/

graph=$1

iterations=1500
test_after=15
procs_per_machine=48
./run_decentalized.sh $graph $procs_per_machine $iterations $test_after
