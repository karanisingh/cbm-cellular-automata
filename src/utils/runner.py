# src/utils/runner.py

# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# from matplotlib.patches import Patch

# import numpy as np
# from celluloid import Camera


'''
Runs the automata
Prints each step in the terminal
Saves a video of the run to the output folder
'''
# def visual_runner(automata, steps, output_path, record, video_length):

#     # Create the color map
#     state_colors = automata.get_state_colors()
#     print("State colors: ", state_colors)
#     cmap = mcolors.ListedColormap([state_colors[state][1] for state in state_colors])
#     print("Color Map:", [state_colors[state][1] for state in state_colors])  # Add this line

#     # Create the plot and legend
#     fig, ax = plt.subplots() 
#     camera = Camera(fig)
#     legend_patches = [Patch(color=color, label=name) for name, color in state_colors.values()]

#     # Initial grid snapshot
#     ax.imshow(automata.current_grid, cmap=cmap)
#     ax.legend(handles=legend_patches, loc='upper left', framealpha=0.04)
#     ax.grid(which='both', color='k', linestyle='-', linewidth=1)
#     ax.set_xticks(np.arange(-.5, automata.current_grid.shape[1], 1))
#     ax.set_yticks(np.arange(-.5, automata.current_grid.shape[0], 1))
#     ax.set_xticklabels([])  # Remove x-axis tick labels
#     ax.set_yticklabels([])  # Remove y-axis tick labels
#     ax.tick_params(axis='both', which='both', length=0)  # Hide the tick marks
#     ax.axis('on')   
#     ax.text(0.95, 0.05, f'Time: {0}', transform=ax.transAxes, color='white',ha='right', va='bottom', fontsize='large', weight='bold',bbox=dict(boxstyle='round,pad=0.1', facecolor='black', edgecolor='none', alpha=0.7))      
#     camera.snap()   
#     ax.clear()

#     # Run for the steps, create the frames for the video
#     for i in range(steps):
#         automata.update_grid()
#         print(f"Step {i+1} of {steps}")
#         print("Automata:\n",automata.current_grid)
#         print("Timer:\n",automata.current_timer_grid, "\n\n")

#         # Grid display
#         ax.imshow(automata.current_grid, cmap=cmap)
#         ax.legend(handles=legend_patches, loc='upper left', framealpha=0.04)
#         ax.grid(which='both', color='k', linestyle='-', linewidth=1)
#         ax.set_xticks(np.arange(-.5, automata.current_grid.shape[1], 1))
#         ax.set_yticks(np.arange(-.5, automata.current_grid.shape[0], 1))
#         ax.set_xticklabels([])  # Remove x-axis tick labels
#         ax.set_yticklabels([])  # Remove y-axis tick labels
#         ax.tick_params(axis='both', which='both', length=0)  # Hide the tick marks
#         ax.axis('on')
#         ax.text(0.95, 0.05, f'Time: {i+1}', transform=ax.transAxes, color='white',ha='right', va='bottom', fontsize='large', weight='bold',bbox=dict(boxstyle='round,pad=0.1', facecolor='black', edgecolor='none', alpha=0.7))      

#         # Save frame    
#         camera.snap()
#         ax.clear()

#         # Check if the automata has been terminated
#         if automata.is_terminated:
#             print("Termination state has been reached.\n")
#             break   

    

#     # Create and save the animation
#     animation = camera.animate()
#     if record:
#         animation.save(output_path, writer='ffmpeg', fps=max(float(steps)/video_length, 1))

#     print(f"Video of the run can be found at {output_path}")

# from matplotlib.animation import FuncAnimation

# # Define the update function for animation
# def update(frame_number, automata, fig, ax, cmap, legend_patches):
#     ax.clear()
#     automata.update_grid()
#     print(f"Step {frame_number+1}")
#     print("Automata:\n",automata.current_grid)
#     print("Timer:\n",automata.current_timer_grid, "\n\n")

#     # Set up the plot settings again
#     ax.imshow(automata.current_grid, cmap=cmap)
#     ax.legend(handles=legend_patches, loc='upper left', framealpha=0.04)
#     ax.grid(which='both', color='k', linestyle='-', linewidth=1)
#     ax.set_xticks(np.arange(-.5, automata.current_grid.shape[1], 1))
#     ax.set_yticks(np.arange(-.5, automata.current_grid.shape[0], 1))
#     ax.set_xticklabels([])  # Remove x-axis tick labels
#     ax.set_yticklabels([])  # Remove y-axis tick labels
#     ax.tick_params(axis='both', which='both', length=0)  # Hide the tick marks
#     ax.axis('on')
#     ax.text(0.95, 0.05, f'Time: {frame_number+1}', transform=ax.transAxes, color='white',ha='right', va='bottom', fontsize='large', weight='bold',bbox=dict(boxstyle='round,pad=0.1', facecolor='black', edgecolor='none', alpha=0.7))      
    
#     # Optionally print the current state of the grid to the terminal
#     print(f"Step {frame_number + 1}")
#     print("Automata:\n", automata.current_grid)
#     print("Timer:\n", automata.current_timer_grid, "\n\n")
    
#     if automata.is_terminated:
#         print("Termination state has been reached.\n")
#         # Stop the animation if the automata is terminated
#         anim.event_source.stop()

# def visual_runner(automata, steps, output_path, record, video_length):
#     # Create the initial plot outside the loop
#     fig, ax = plt.subplots()
#     state_colors = automata.get_state_colors()
#     print("State colors: ", state_colors)
#     cmap = mcolors.ListedColormap([state_colors[state][1] for state in state_colors])
#     legend_patches = [Patch(color=color, label=name) for name, color in state_colors.values()]

#     # Create the animation object
#     anim = FuncAnimation(fig, update, fargs=(automata, fig, ax, cmap, legend_patches), frames=steps, repeat=False)

#     # Save the animation
#     if record:
#         anim.save(output_path, writer='ffmpeg', fps=max(float(steps)/video_length, 1))

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
import imageio
import os

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
