#!/bin/bash
#BSUB -q hpc
#BSUB -W 01:30
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2048MB]"
#BSUB -J ex6_scaling
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -o job_ex6/scalingN_dyn_%J.out
#BSUB -e job_ex6/scalingN_dyn_%J.err

source /dtu/projects/02613_2026/conda/conda_init.sh
conda activate 02613_2026

echo "Starting Dynamic Scaling Test for N=100 floorplans"
echo "-------------------------------------------------"

for N in 10 20 30 40; do
    for w in 1 2 4 8 16; do
        time python -u ex5.py $N $w
    done
done

echo "-------------------------------------------------"
echo "Done!"