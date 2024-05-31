#!/bin/bash

cd ../

source .venv/bin/activate

cd tutorial/

iterations=1000
test_after=10
procs_per_machine=48

generate_graphs() {
    python generate_graph.py --nodes=48 --highMobilityProportion=0
    python generate_graph.py --nodes=48 --highMobilityProportion=0.05
    python generate_graph.py --nodes=48 --highMobilityProportion=0.2
    python generate_graph.py --nodes=48 --highMobilityProportion=0.4
    python generate_graph.py --nodes=48 --highMobilityProportion=0.6
    python generate_graph.py --nodes=48 --highMobilityProportion=0.8
    python generate_graph.py --nodes=48 --highMobilityProportion=1.0
}

run_experiment() {
    (cd .. && generate_graphs)

    ./run_decentralized.sh dynamic_48_0_0.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_05.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_2.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_4.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_6.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_8.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_1_0.txt $procs_per_machine $iterations $test_after
}

run_experiment

run_experiment

# run_experiment

# Shutdown
sudo shutdown -h now
