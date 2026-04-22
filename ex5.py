import sys
import time
import numpy as np
import multiprocessing as mp
from os.path import join
from simulate import jacobi, load_data, summary_stats

def worker(building_ids_chunk, load_dir, max_iter, abs_tol):
    """Processes a static chunk of buildings on a single worker."""
    chunk_results = []
    for bid in building_ids_chunk:
        u0, mask = load_data(load_dir, bid)
        u_final = jacobi(u0, mask, max_iter, abs_tol)
        stats = summary_stats(u_final, mask)
        chunk_results.append((bid, stats))
    return chunk_results

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    
    # Call as: python parallel_simulate.py <N> <num_workers>
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    # Split data into static chunks
    chunks = np.array_split(building_ids, num_workers)
    
    start_time = time.perf_counter()
    
    # Run parallel pool
    with mp.Pool(num_workers) as pool:
        # Static assignment: each worker gets a fixed chunk 
        results_of_chunks = pool.starmap(worker, 
                                        [(chunk, LOAD_DIR, MAX_ITER, ABS_TOL) for chunk in chunks])
    
    end_time = time.perf_counter()
    total_time = end_time - start_time

    final_results = [item for sublist in results_of_chunks for item in sublist]

    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print(f"Workers: {num_workers} | Execution time: {total_time:.4f} seconds")
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    
    for bid, stats in final_results:
        print(f"{bid}, " + ", ".join(str(stats[k]) for k in stat_keys))
