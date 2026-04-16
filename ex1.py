from os.path import join
import sys
import numpy as np
import matplotlib.pyplot as plt
import simulate

LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'

u, interior_mask = simulate.load_data(LOAD_DIR,10000)

def plot_heatmap(data, name):
    """
    Plots a heatmap for the given data and saves it with a dynamic name.
    
    Args:
        data (numpy.ndarray): The matrix to visualize (u or interior_mask).
        name (str): The name to use for the title and the saved file.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Use the data passed as argument, not a hardcoded variable
    heatmap = ax.imshow(data, cmap='magma', interpolation='nearest')
    
    cbar = fig.colorbar(heatmap)
    cbar.set_label('Value Intensity')
    
    # Dynamic title and labels
    ax.set_title(f"Heatmap - {name}")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")

    # Save using the provided name
    file_path = f"ex1_{name}.svg"
    plt.savefig(file_path)
    print(f"Figure saved as: {file_path}")
    
    plt.close(fig) # Close to free up memory during tests

# Usage examples:
plot_heatmap(u, "u")
plot_heatmap(interior_mask, "interior_mask")