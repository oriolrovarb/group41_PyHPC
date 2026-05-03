#!/bin/sh
#BSUB -q gpuv100
#BSUB -J gpu_sim_100
#BSUB -W 00:30
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -N 
#BSUB -o gpu_100_%J.out
#BSUB -e gpu_100_%J.err

source /dtu/projects/02613_2026/conda/conda_init.sh
conda activate 02613_2026

echo "Starting GPU Execution for N=100 floorplans"
echo "-------------------------------------------------"

python -u ex9.py 100

echo "-------------------------------------------------"
echo "Done!"