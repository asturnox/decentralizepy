#!/bin/bash

iterations=200
test_after=10
procs_per_machine=48
run_decentalized.sh dynamic_48_0_2.txt $procs_per_machine $iterations $test_after
run_decentalized.sh dynamic_48_0_4.txt $procs_per_machine $iterations $test_after
run_decentalized.sh dynamic_48_0_6.txt $procs_per_machine $iterations $test_after
run_decentalized.sh dynamic_48_0_8.txt $procs_per_machine $iterations $test_after
