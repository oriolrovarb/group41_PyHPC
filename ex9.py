import sys
import time
import cupy as cp
import numpy as np
from os.path import join
from simulate import load_data, summary_stats

def jacobi_cupy(u0, mask, max_iter, abs_tol):
    """GPU-accelerated Jacobi iteration using CuPy."""
    # 1. Transfer data from Host (CPU) to Device (GPU)
    u_gpu = cp.asarray(u0)
    mask_gpu = cp.asarray(mask)
    u0_gpu = cp.asarray(u0) # Preserve initial state for boundaries
    
    for i in range(max_iter):
        u_old = u_gpu.copy()
        
        # 2. Core Jacobi update (vectorized)
        u_gpu[1:-1, 1:-1] = 0.25 * (u_old[:-2, 1:-1] + u_old[2:, 1:-1] + 
                                    u_old[1:-1, :-2] + u_old[1:-1, 2:])
        
        # 3. Enforce boundary conditions
        u_gpu[~mask_gpu] = u0_gpu[~mask_gpu]
        
        # 4. Convergence check
        # Note: Evaluating this every single loop causes sync overhead (see below)
        if cp.max(cp.abs(u_gpu - u_old)) < abs_tol:
            break
            
    # 5. Transfer result back to Host (CPU)
    return cp.asnumpy(u_gpu)

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    
    # Call as: python gpu_simulate.py <N>
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    start_time = time.perf_counter()
    
    results = []
    # Process sequentially on CPU, offloading matrix math to the GPU
    for bid in building_ids:
        # I/O and setup remain on CPU
        u0, mask = load_data(LOAD_DIR, bid)
        
        # Heavy compute on GPU
        u_final = jacobi_cupy(u0, mask, MAX_ITER, ABS_TOL)
        
        # Summary stats handled back on CPU
        stats = summary_stats(u_final, mask)
        results.append((bid, stats))
    
    end_time = time.perf_counter()
    total_time = end_time - start_time

    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print(f"GPU Execution | Total time: {total_time:.4f} seconds")
    print('building_id, ' + ', '.join(stat_keys))
    
    for bid, stats in results:
        print(f"{bid}, " + ", ".join(str(stats[k]) for k in stat_keys))