#!/bin/bash
#BSUB -J WallHeating_Batch_2
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:30
#BSUB -R "rusage[mem=8GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -o WallHeating_Batch_2_%J.out
#BSUB -e WallHeating_Batch_2_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

echo "-------------------------------------------"
echo "Running Wall Heating implementation from index 1524 to 3048"
echo "-------------------------------------------"

time python ex8_gpu.py 1524 3048 > results_batch_2.csv
