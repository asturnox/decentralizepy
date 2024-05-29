#!/bin/bash
graph=$1 # Absolute path of the graph file generated using the generate_graph.py script
procs_per_machine=$2 # Number of processes per machine
iterations=$3
test_after=$4

path=$(pwd)
decpy_path=$path/../eval # Path to eval folder
run_path=$path/../eval/data # Path to the folder where the graph and config file will be copied and the results will be stored
config_file=config.ini
echo $run_path
echo $decpy_path
cp $graph $config_file $run_path

env_python=../.venv/bin/python3 # Path to python executable of the environment | conda recommended
machines=1 # number of machines in the runtime
eval_file=$decpy_path/testingPeerSamplerDynamic.py # decentralized driver code (run on each machine)
log_level=DEBUG # DEBUG | INFO | WARN | CRITICAL

m=0 # machine id corresponding consistent with ip.json
echo M is $m

echo procs per machine is $procs_per_machine

log_dir=$run_path/$(date '+%Y-%m-%dT%H:%M')/machine$m # in the eval folder
mkdir -p $log_dir

$env_python $eval_file -ro 0 -tea $test_after -ld $log_dir -mid $m -ps $procs_per_machine -ms $machines -is $iterations -gf $run_path/$graph -ta $test_after -cf $run_path/$config_file -ll $log_level -wsd $log_dir