import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Configuration & Data
# ---------------------------------------------------------
workers = [1, 2, 4, 8, 16]
n_values = [10, 20, 30, 40]

# Execution times in seconds extracted from the dynamic logs
execution_times_dyn = {
    10: [81.4636, 49.4198, 30.3307, 29.8599, 15.9293],
    20: [204.3978, 125.2546, 67.1017, 44.1378, 39.3701],
    30: [269.1701, 146.4982, 90.5960, 54.2336, 42.1596],
    40: [379.1917, 203.0097, 126.3734, 76.4835, 67.3494]
}

# Execution times in seconds extracted from the static logs
execution_times_stat = {
    10: [80.0226, 48.3109, 29.2805, 30.2098, 15.5626],
    20: [208.8035, 127.1186, 68.3605, 43.7968, 40.4294],
    30: [272.1529, 149.5831, 88.9725, 53.4100, 42.4210],
    40: [371.4055, 203.6482, 125.7235, 74.8180, 72.8450]
}

# Define colormaps to distinguish different N values easily
colors_dyn = ['#a1d99b', '#74c476', '#31a354', '#006d2c'] # Green shades
colors_stat = ['#9ecae1', '#6baed6', '#3182bd', '#08519c'] # Blue shades

# ---------------------------------------------------------
# 2. Helper Functions
# ---------------------------------------------------------
def calculate_speedups(base_time, times):
    """
    Calculates the speed-up given a base time (T1) and a list of execution times.
    """
    return [base_time / t for t in times]

def plot_multi_n_scaling(workers, execution_times, title, colors, save_path):
    """
    Generates a single standalone SVG plot displaying scaling curves for multiple N values.
    """
    plt.figure(figsize=(9, 6))
    
    # Iterate through each N value and plot its speedup
    for i, n in enumerate(n_values):
        times = execution_times[n]
        base_time = times[0]
        speedups = calculate_speedups(base_time, times)
        
        plt.plot(
            workers, 
            speedups, 
            marker='o', 
            color=colors[i], 
            label=f'N={n}'
        )
    
    # Plot ideal linear scaling reference
    plt.plot(workers, workers, linestyle='--', color='gray', label='Ideal Linear Scaling')
    
    # Format labels, title, and layout
    plt.title(f'{title} Scheduling Scaling Test', fontsize=14, pad=15)
    plt.xlabel('Number of Workers', fontsize=12)
    plt.ylabel('Speed-up', fontsize=12)
    plt.xticks(workers)
    
    # Grid and legend configuration
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper left', title="Workload (N)")
    
    # Save the plot securely to disk as SVG
    plt.tight_layout()
    plt.savefig(save_path, format='svg')
    plt.close()

# ---------------------------------------------------------
# 3. Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    
    # Generate Separate Static Plot
    plot_multi_n_scaling(
        workers=workers, 
        execution_times=execution_times_stat, 
        title='Static', 
        colors=colors_stat, 
        save_path='scaling_static.svg'
    )
    
    # Generate Separate Dynamic Plot
    plot_multi_n_scaling(
        workers=workers, 
        execution_times=execution_times_dyn, 
        title='Dynamic', 
        colors=colors_dyn, 
        save_path='scaling_dynamic.svg'
    )
    
    print("Multi-N SVG plots for Static and Dynamic scheduling generated successfully.")