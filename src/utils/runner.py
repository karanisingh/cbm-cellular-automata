import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
import imageio
import os

'''
Runs the automata
Prints each step in the terminal
Saves a video of the run to the output folder
'''

def visual_runner(automata, steps, output_path, record, video_length):
    # Create a temporary directory to store images
    if not os.path.exists('temp_images'):
        os.makedirs('temp_images')

    # State colors from automata
    state_colors = automata.get_state_colors()
    color_map = {state: mcolors.to_rgba(color) for state, (_, color) in state_colors.items()}
    legend_patches = [mpatches.Patch(color=color, label=label) for _, (label, color) in state_colors.items()]
    nrows, ncols = automata.current_grid.shape

    # Generate images for each step
    for step in range(steps):
        print(f"Step {step}")
        print("Automata:\n", automata.current_grid)
        print("Timer:\n", automata.current_timer_grid, "\n\n")
        fig, ax = plt.subplots()
        ax.set_title(f"Step {step}")
        # Create a grid image with colors based on state
        grid_image = [[color_map[state] for state in row] for row in automata.current_grid]
        ax.imshow(grid_image, interpolation='nearest', aspect='auto')

        # Set aspect of the plot to be equal to ensure square cells
        ax.set_aspect('equal')

        # Adding grid lines
        ax.vlines(np.arange(ncols) - 0.5, ymin=-0.5, ymax=nrows - 0.5, color='white', linewidth=2)
        ax.hlines(np.arange(nrows) - 0.5, xmin=-0.5, xmax=ncols - 0.5, color='white', linewidth=2)

        # Adding legend inside the plot
        ax.legend(handles=legend_patches, loc='upper right')
        
        # Accommodate for device and no device
        for (i, j), value in np.ndenumerate(automata.device_grid):
            if value == 1:  # If a device is present
                if(automata.current_grid[i][j] == automata.State.EXPOSED.value):
                    ax.text(j, i, 'D', ha='center', va='center', color='black', fontsize='large', fontweight='bold')
                else:
                    ax.text(j, i, 'D', ha='center', va='center', color='white', fontsize='large', fontweight='bold')


        # Remove axis ticks
        ax.axis('off')
        plt.savefig(f'temp_images/step_{step}.png', bbox_inches='tight')
        plt.close()

        # Update the automata for the next step
        automata.update_grid()

    # Compile images into a video
    with imageio.get_writer(output_path, fps=max(float(steps)/video_length, 1)) as video:
        for step in range(steps):
            image = imageio.imread(f'temp_images/step_{step}.png')
            video.append_data(image)

    # Clean up temporary images
    for step in range(steps):
        os.remove(f'temp_images/step_{step}.png')
    os.rmdir('temp_images')

    print(f"Video saved to {output_path}")







    # # Device colors from automata
    # device_colors = automata.get_device_colors()
    # d_color_map = {device: mcolors.to_rgba(color) for device, (_, color) in device_colors.items()}
    # d_legend_patches = [mpatches.Patch(color=color, label=label) for _, (label, color) in device_colors.items()]
