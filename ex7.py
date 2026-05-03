import sys
import time
import numpy as np
from os.path import join
from numba import njit
from simulate import load_data, summary_stats

@njit # CPU JIT @jit(nopython=True)
def jacobi_numba(u, interior_mask, max_iter, atol=1e-6):
    """
    Optimized Jacobi solver using Numba JIT.
    Loops are structured to ensure row-major (C-style) memory access.
    """
    # Create a copy to avoid modifying the input array in-place unexpectedly
    u_curr = u.copy()
    u_next = u.copy()
    
    # Pre-calculate dimensions for the loops
    rows, cols = u_curr.shape
    
    for iteration in range(max_iter):
        delta = 0.0
        
        # Iterate over the interior of the 514x514 grid
        # The mask is 512x512, corresponding to u[1:-1, 1:-1]
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Only update if the point is an interior room point
                if interior_mask[i-1, j-1]:
                    # Standard Jacobi average of 4 neighbors
                    val = 0.25 * (u_curr[i, j-1] + u_curr[i, j+1] + 
                                  u_curr[i-1, j] + u_curr[i+1, j])
                    
                    # Calculate local convergence delta
                    diff = abs(val - u_curr[i, j])
                    if diff > delta:
                        delta = diff
                    
                    u_next[i, j] = val
        
        # Update u_curr for the next iteration
        # Using u_curr[:] = u_next[:] is fast in Numba
        u_curr[:] = u_next[:]
        
        # Early stopping check
        if delta < atol:
            break
            
    return u_curr

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000 
    ABS_TOL = 1e-4 
    
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
        u_final = jacobi_numba(u0, mask, MAX_ITER, ABS_TOL)
        
        stats = summary_stats(u_final, mask)
        print(f"{bid}, " + ", ".join(f"{stats[k]:.4f}" for k in stat_keys))
    
    end_time = time.perf_counter()
    print(f"\nTotal execution time for {N} buildings: {end_time - start_time:.4f} seconds")