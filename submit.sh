#!/bin/bash
#BSUB -J timer_10
#BSUB -q hpc
#BSUB -W 00:10
#BSUB -n 1
#BSUB -R "rusage[mem=1024MB]"
#BSUB -B
#BSUB -N
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -o timer20_%J.out
#BSUB -e timer20_%J.err

# Run and time the script for N=10
time python3 simulate.py 20