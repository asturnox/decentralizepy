#!/bin/bash

cd ../

cd tutorial/

graph=$1

iterations=1000
test_after=10
procs_per_machine=48
./run_decentralized.sh $graph $procs_per_machine $iterations $test_after
