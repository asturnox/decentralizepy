#!/bin/sh
#
#SBATCH --job-name="decentralizepy"
#SBATCH --partition=compute
#SBATCH --time=20:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=8G

filename=$1
srun deploy.sh $filename