#!/bin/bash

cd ../

source .venv/bin/activate

cd tutorial/

iterations=4000
test_after=40
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

    alpha=$1
    sed -i'' -e "s/^alpha=.*/alpha=${alpha}/" config.ini

    current_time=$(date +"%Y-%m-%dT%H:%M")
    mkdir "../eval/data/${current_time}-${alpha}"

    sync

    ./run_decentralized.sh dynamic_48_0_0.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_05.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_2.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_4.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_6.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_0_8.txt $procs_per_machine $iterations $test_after
    ./run_decentralized.sh dynamic_48_1_0.txt $procs_per_machine $iterations $test_after
}

run_experiments() {
    run_experiment 0.1
    # run_experiment 0.2
    run_experiment 0.3
    # run_experiment 0.4
}

run_experiments

run_experiments

run_experiments

# Shutdown
sudo shutdown -h now
