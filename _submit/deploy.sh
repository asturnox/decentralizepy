#!/bin/bash

cd ../

cd tutorial/

iterations=1000
test_after=10
procs_per_machine=48
./run_decentralized.sh dynamic_48_0_0.txt $procs_per_machine $iterations $test_after
./run_decentralized.sh dynamic_48_0_05.txt $procs_per_machine $iterations $test_after
./run_decentralized.sh dynamic_48_0_2.txt $procs_per_machine $iterations $test_after
./run_decentralized.sh dynamic_48_0_4.txt $procs_per_machine $iterations $test_after
# ./run_decentralized.sh dynamic_48_0_6.txt $procs_per_machine $iterations $test_after
# ./run_decentralized.sh dynamic_48_0_8.txt $procs_per_machine $iterations $test_after
./run_decentralized.sh dynamic_48_1_0.txt $procs_per_machine $iterations $test_after
