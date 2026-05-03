#!/bin/bash
#BSUB -J profiler
#BSUB -q hpc
#BSUB -W 00:10
#BSUB -n 1
#BSUB -R "rusage[mem=1024MB]"
#BSUB -N
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -o timer20_%J.out
#BSUB -e timer20_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

kernprof -l -v ex4.py