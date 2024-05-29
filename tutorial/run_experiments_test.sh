#!/bin/bash

iterations=5
test_after=2
procs_per_machine=12
./run_decentralized.sh dynamic_12_0_2.txt $procs_per_machine $iterations $test_after
./run_decentralized.sh dynamic_12_0_8.txt $procs_per_machine $iterations $test_after
