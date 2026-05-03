#!/bin/bash
#BSUB -J CPU_Numba
#BSUB -q hpc
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -W 10:00                  
#BSUB -R "rusage[mem=4GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -o CPU_Numba_%J.out
#BSUB -e CPU_Numba_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

for N in 32 64 128 256 512
do 
    echo "-------------------------------------------"
    echo "Running Numba implementation with N=$N"
    echo "-------------------------------------------"
    python3 ex7.py $N
done