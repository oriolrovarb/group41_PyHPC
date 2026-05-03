#!/bin/bash
#BSUB -J Numba_Scaling
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:30
#BSUB -R "rusage[mem=8GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -o gpu_%J.out
#BSUB -e gpu_%J.err

# Load the required Conda environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

# Iterate over the specified batch sizes
for N in 10 20 30 40 50
do 
    echo "-------------------------------------------"
    echo "Running Numba implementation with N=$N"
    echo "-------------------------------------------"
    time python3 ex8.py $N
done