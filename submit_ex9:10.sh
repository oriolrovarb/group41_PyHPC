#!/bin/sh
#BSUB -q c02613
#BSUB -J gpujob
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -u s253020@dtu.dk
#BSUB -o gpujob_%J.out
#BSUB -e gpujob_%J.err


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

for N in 10 20 30 50 
do
    nsys profile -o report_$N python3 ex_9.py $N
done