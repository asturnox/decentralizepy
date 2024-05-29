#!/bin/sh
#
#SBATCH --job-name="decentralizepy"
#SBATCH --partition=compute
#SBATCH --time=4:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=4G

srun deploy.sh