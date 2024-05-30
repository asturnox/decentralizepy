#!/bin/bash

python generate_graph.py --nodes=48 --highMobilityProportion=0
python generate_graph.py --nodes=48 --highMobilityProportion=0.05
python generate_graph.py --nodes=48 --highMobilityProportion=0.2
python generate_graph.py --nodes=48 --highMobilityProportion=0.4
python generate_graph.py --nodes=48 --highMobilityProportion=0.6
python generate_graph.py --nodes=48 --highMobilityProportion=0.8
python generate_graph.py --nodes=48 --highMobilityProportion=1.0

