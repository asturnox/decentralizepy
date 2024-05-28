#!/bin/sh
#
#SBATCH --job-name="decentralizepy"
#SBATCH --partition=compute-p2
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=64G

filename=$1

srun deploy.sh dynamic_12_0_2.txt