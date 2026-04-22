#!/bin/bash
#BSUB -J static_scaling
#BSUB -q hpc
#BSUB -W 00:30
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2048MB]"
#BSUB -N
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -o scaling100_%J.out
#BSUB -e scaling100_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2025

echo "Starting Static Scaling Test for N=100 floorplans"
echo "-------------------------------------------------"

for w in 1 2 4 8 16; do
    python -u ex5.py 100 $w
done

echo "-------------------------------------------------"
echo "Done!"