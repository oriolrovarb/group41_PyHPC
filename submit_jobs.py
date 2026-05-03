import math
import os
import subprocess

def generate_and_submit():
    # Dataset specs
    total_buildings = 4571
    num_batches = 3
    chunk_size = math.ceil(total_buildings / num_batches)
    
    for i in range(num_batches):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_buildings)
        
        job_name = f"WallHeating_Batch_{i+1}"
        script_filename = f"submit_ex12_{i+1}.sh"
        
        # Build the shell script content dynamically
        sh_content = f"""#!/bin/bash
#BSUB -J {job_name}
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:30
#BSUB -R "rusage[mem=8GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -o {job_name}_%J.out
#BSUB -e {job_name}_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

echo "-------------------------------------------"
echo "Running Wall Heating implementation from index {start_idx} to {end_idx}"
echo "-------------------------------------------"

time python ex8_gpu.py {start_idx} {end_idx} > results_batch_{i+1}.csv
"""
        
        # Write the shell script to disk
        with open(script_filename, 'w') as f:
            f.write(sh_content)
            
        # Submit the job to the cluster
        print(f"Submitting {script_filename} (Buildings {start_idx} to {end_idx})...")
        try:
            # Pass the whole command as a single formatted string
            subprocess.run(f"bsub < {script_filename}", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error submitting {script_filename}: {e}")

if __name__ == '__main__':
    generate_and_submit()