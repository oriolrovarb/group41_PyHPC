import sys
import time
import numpy as np
from os.path import join
from numba import cuda
import math
from simulate import load_data, summary_stats

# # --- CUDA Kernel ---
# @cuda.jit
# def jacobi_kernel(u_curr, u_next, interior_mask):
#     # Determine the absolute position of the thread in the 2D grid
#     i, j = cuda.grid(2)
    
#     # Boundary check: ensure thread is within the interior of the 514x514 grid
#     # u_curr.shape[0]-1 corresponds to 513
#     if 1 <= i < u_curr.shape[0] - 1 and 1 <= j < u_curr.shape[1] - 1:
#         # Check the mask (mask is 512x512, indexed from 0)
#         if interior_mask[i-1, j-1]:
#             # Perform the Jacobi update for one cell
#             u_next[i, j] = 0.25 * (u_curr[i, j-1] + u_curr[i, j+1] + 
#                                    u_curr[i-1, j] + u_curr[i+1, j])
#         else:
#             # For walls/outside, keep the existing value
#             u_next[i, j] = u_curr[i, j]

@cuda.jit
def jacobi_kernel(u_curr, u_next, interior_mask):
    i, j = cuda.grid(2)
    
    # Strictly check bounds: we need 1 pixel of padding for neighbors (i-1, i+1, etc.)
    # and we must stay within the 512x512 mask bounds.
    if 1 <= i < u_curr.shape[0] - 1 and 1 <= j < u_curr.shape[1] - 1:
        # The mask is exactly 512x512, mapped to the interior 1:513
        m_i = i - 1
        m_j = j - 1
        
        # Verify mask indexing is safe
        if m_i < interior_mask.shape[0] and m_j < interior_mask.shape[1]:
            if interior_mask[m_i, m_j]:
                u_next[i, j] = 0.25 * (u_curr[i, j-1] + u_curr[i, j+1] + 
                                       u_curr[i-1, j] + u_curr[i+1, j])
            else:
                u_next[i, j] = u_curr[i, j]

# --- Helper Function ---
def run_jacobi_cuda(u0, interior_mask, max_iter):
    # 1. Transfer data to the GPU device
    d_u_curr = cuda.to_device(u0)
    d_u_next = cuda.to_device(u0)
    d_mask = cuda.to_device(interior_mask)
    
    # 2. Define block and grid dimensions
    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(u0.shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(u0.shape[1] / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
    
    # 3. Iteratively call the kernel
    for _ in range(max_iter):
        jacobi_kernel[blocks_per_grid, threads_per_block](d_u_curr, d_u_next, d_mask)
        # Swap pointers for the next iteration (avoids re-copying data)
        d_u_curr, d_u_next = d_u_next, d_u_curr
    
    # 4. Copy the final result back to the host (CPU)
    return d_u_curr.copy_to_host()

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000 
    
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    print(f"Processing {N} buildings using Numba JIT...")
    start_time = time.perf_counter()
    
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))
    
    for bid in building_ids:
        u0, mask = load_data(LOAD_DIR, bid)
        
        # Calling the JIT-optimized function 
        u_final = run_jacobi_cuda(u0, mask, MAX_ITER)
        
        stats = summary_stats(u_final, mask)
        print(f"{bid}, " + ", ".join(f"{stats[k]:.4f}" for k in stat_keys))
    
    end_time = time.perf_counter()
    print(f"\nTotal execution time for {N} buildings: {end_time - start_time:.4f} seconds")