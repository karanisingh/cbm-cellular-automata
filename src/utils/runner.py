# src/utils/runner.py

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

import numpy as np
from celluloid import Camera


'''
Runs the automata
Prints each step in the terminal
Saves a video of the run to the output folder
'''
def visual_runner(automata, steps, output_path, record, video_length):

    # Create the color map
    state_colors = automata.get_state_colors()
    cmap = mcolors.ListedColormap([state_colors[state][1] for state in state_colors])
    print("Color Map:", [state_colors[state][1] for state in state_colors])  # Add this line

    # Create the plot and legend
    fig, ax = plt.subplots() 
    camera = Camera(fig)
    legend_patches = [Patch(color=color, label=name) for name, color in state_colors.values()]

    # Initial grid snapshot
    ax.imshow(automata.current_grid, cmap=cmap)
    ax.legend(handles=legend_patches, loc='upper left', framealpha=0.04)
    ax.grid(which='both', color='k', linestyle='-', linewidth=1)
    ax.set_xticks(np.arange(-.5, automata.current_grid.shape[1], 1))
    ax.set_yticks(np.arange(-.5, automata.current_grid.shape[0], 1))
    ax.set_xticklabels([])  # Remove x-axis tick labels
    ax.set_yticklabels([])  # Remove y-axis tick labels
    ax.tick_params(axis='both', which='both', length=0)  # Hide the tick marks
    ax.axis('on')   
    ax.text(0.95, 0.05, f'Time: {0}', transform=ax.transAxes, color='white',ha='right', va='bottom', fontsize='large', weight='bold',bbox=dict(boxstyle='round,pad=0.1', facecolor='black', edgecolor='none', alpha=0.7))      
    camera.snap()    

    # Run for the steps, create the frames for the video
    for i in range(steps):
        automata.update_grid()
        print(f"Step {i+1} of {steps}")
        print(automata.current_grid, "\n\n")

        # Grid display
        ax.imshow(automata.current_grid, cmap=cmap)
        #ax.legend(handles=legend_patches, loc='upper left', framealpha=0.05)
        ax.grid(which='both', color='k', linestyle='-', linewidth=1)
        ax.set_xticks(np.arange(-.5, automata.current_grid.shape[1], 1))
        ax.set_yticks(np.arange(-.5, automata.current_grid.shape[0], 1))
        ax.set_xticklabels([])  # Remove x-axis tick labels
        ax.set_yticklabels([])  # Remove y-axis tick labels
        ax.tick_params(axis='both', which='both', length=0)  # Hide the tick marks
        ax.axis('on')
        ax.text(0.95, 0.05, f'Time: {i+1}', transform=ax.transAxes, color='white',ha='right', va='bottom', fontsize='large', weight='bold',bbox=dict(boxstyle='round,pad=0.1', facecolor='black', edgecolor='none', alpha=0.7))      

        # Save frame    
        camera.snap()

        # Check if the automata has been terminated
        if automata.is_terminated:
            print("Termination state has been reached.\n")
            break   

    

    # Create and save the animation
    animation = camera.animate()
    if record:
        animation.save(output_path, writer='ffmpeg', fps=max(float(steps)/video_length, 1))

    print(f"Video of the run can be found at {output_path}")

