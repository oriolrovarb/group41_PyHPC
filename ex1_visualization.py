import os
import matplotlib.pyplot as plt
import simulate

def plot_heatmap(data, name, output_dir="."):
    """
    Plots a heatmap for the given matrix and saves it to a specified directory.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Render the heatmap
    heatmap = ax.imshow(data, cmap='magma', interpolation='nearest')
    
    # Configure the colorbar
    cbar = fig.colorbar(heatmap)
    cbar.set_label('Value Intensity')
    
    # Set dynamic titles and axis labels
    ax.set_title(f"Heatmap - {name}")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the file path and save the figure
    file_path = os.path.join(output_dir, f"{name}.svg")
    plt.savefig(file_path)
    print(f"Figure saved as: {file_path}")
    
    # Free up memory to prevent leaks during batch processing
    plt.close(fig) 

def process_floor_plans(base_dir, plan_ids, output_dir="results"):
    """
    Iterates over a list of floor plan IDs, loads their simulation data, 
    and generates the corresponding heatmaps.
    """
    for plan_id in plan_ids:
        print(f"Processing floor plan ID: {plan_id}...")
        try:
            # Load the specific floor plan data
            u, interior_mask = simulate.load_data(base_dir, plan_id)
            
            # Plot and save both the simulation output and the mask
            plot_heatmap(u, f"ex1_u_plan_{plan_id}", output_dir)
            plot_heatmap(interior_mask, f"ex1_interior_mask_plan_{plan_id}", output_dir)
            
        except Exception as e:
            # Catch errors (e.g., missing files) so the loop does not crash
            print(f"Failed to process plan {plan_id}: {e}")

if __name__ == "__main__":
    # Define configuration paths
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    OUTPUT_DIR = 'simulation_plots'
    
    # List of floor plan indices you want to simulate and plot
    plans_to_test = [10000, 10001, 10002, 10003]
    
    # Run the pipeline
    process_floor_plans(LOAD_DIR, plans_to_test, OUTPUT_DIR)