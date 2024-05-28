#!/bin/sh
#
#SBATCH --job-name="decentralizepy"
#SBATCH --partition=compute
#SBATCH --time=20:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=4G

filename=$1
srun deploy.sh $filename