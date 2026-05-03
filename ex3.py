import os
import matplotlib.pyplot as plt
import simulate

def plot_12_grid_final(simulation_results, output_dir="results"):
    """
    Plots 4 floor plans with 3 vertical visualizations each (12 plots total).
    Row 1: Interior Mask
    Row 2: Initial Simulated Heatmap (T=0)
    Row 3: Final Simulated Heatmap
    """
    # Restrict to exactly 4 plans for the grid layout
    plan_ids = list(simulation_results.keys())[:4]
    
    # Create a 3 rows by 4 columns grid (12 plots total)
    fig, axes = plt.subplots(3, 4, figsize=(20, 16))
    fig.suptitle("Exercise 3: Heat Diffusion Analysis", fontsize=24, y=1.02)
    
    for col, plan_id in enumerate(plan_ids):
        data = simulation_results[plan_id]
        u_final = data['u_final']
        mask = data['mask']
        u_initial = data['u_initial']
        
        # --- Row 0: Interior Mask ---
        ax_mask = axes[0, col]
        ax_mask.imshow(mask, cmap='viridis', interpolation='nearest')
        ax_mask.set_title(f"Plan {plan_id}\n1. Interior Mask", fontsize=16)
        ax_mask.axis('off')

        # --- Row 1: Initial Heat Distribution ---
        ax_wall = axes[1, col]
        # Fix: Use ax_wall instead of ax_heat to draw the initial state
        im_wall = ax_wall.imshow(u_initial, cmap='magma', interpolation='nearest')
        ax_wall.set_title("2. Initial Heatmap", fontsize=16)
        ax_wall.axis('off')
        
        # Add colorbar only to the heatmaps to avoid cluttering
        fig.colorbar(im_wall, ax=ax_wall, fraction=0.046, pad=0.04, label='Temp (°C)')
        
        # --- Row 2: Final Diffused Heatmap ---
        ax_heat = axes[2, col]
        im_heat = ax_heat.imshow(u_final, cmap='magma', interpolation='nearest')
        # Fix: Updated title numbering to 3
        ax_heat.set_title("3. Final Heatmap", fontsize=16)
        ax_heat.axis('off')
        
        # Add colorbar matching your requested snippet
        cbar = fig.colorbar(im_heat, ax=ax_heat, fraction=0.046, pad=0.04)
        cbar.set_label('Temp (°C)')
        
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    
    # Save using a dynamic path
    file_path = os.path.join(output_dir, "ex3_12_plots_simulated.svg")
    plt.savefig(file_path, bbox_inches='tight')
    print(f"Figure saved as: {file_path}")
    
    # Free up memory
    plt.close(fig)

def run_and_visualize_batch(base_dir, plan_ids, output_dir="results"):
    """
    Collects simulation data, runs the Jacobi solver, and triggers plotting.
    """
    simulation_results = {}
    
    MAX_ITER = 20000
    ABS_TOL = 1e-4
    
    for plan_id in plan_ids:
        print(f"Processing floor plan ID: {plan_id}...")
        try:
            # Load the initial state from your files
            u_initial, interior_mask = simulate.load_data(base_dir, plan_id)
            
            # Keep a copy of the initial state before modifying it
            u_initial_copy = u_initial.copy()
            
            print(f"  -> Running Jacobi simulation...")
            
            # Execute the actual solver to mathematically diffuse the heat
            u_final = simulate.jacobi(u_initial, interior_mask, MAX_ITER, ABS_TOL)
            
            # Store the final results and the initial copy for plotting
            simulation_results[plan_id] = {
                'u_final': u_final,
                'mask': interior_mask,
                'u_initial': u_initial_copy
            }
            
        except Exception as e:
            print(f"Failed to process plan {plan_id}: {e}")
            
    if len(simulation_results) >= 4:
        plot_12_grid_final(simulation_results, output_dir)
    else:
        print("Warning: Need at least 4 successful plans to generate the grid.")

if __name__ == "__main__":
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    OUTPUT_DIR = 'simulation_results'
    
    # 4 floor plans to fill the 3x4 grid perfectly
    sample_plans = [10000, 10009, 10014, 10019]
    
    print("Starting batch simulation and plotting for 12-grid layout...")
    run_and_visualize_batch(LOAD_DIR, sample_plans, OUTPUT_DIR)
    print("Process complete.")