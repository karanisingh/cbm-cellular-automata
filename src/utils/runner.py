import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import imageio
import csv
import os

'''
Runs the automata
Prints each step in the terminal
Saves a video of the run to the output folder
'''

def visual_runner(automata, steps, output_path, record, video_length):
    # Create a temporary directory to store images
    temp_image_dir = 'temp_images'
    if not os.path.exists('temp_images'):
        os.makedirs('temp_images')

    # State colors from automata
    state_colors = automata.get_state_colors()
    color_map = {state: mcolors.to_rgba(color) for state, (_, color) in state_colors.items()}
    legend_patches = [mpatches.Patch(color=color, label=label) for _, (label, color) in state_colors.items()]
    nrows, ncols = automata.current_grid.shape

    #with open('data\output\last_run_state_counts.csv', 'w', newline='') as csvfile:
    with open(os.path.join('data', 'output', 'last_run_state_counts.csv'), 'w', newline='') as csvfile:

        # output a csv containing the distribution of cells in each state per time step
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["step","s","e","i","q","r","d","total","total_infected"])
        # Generate images for each step
        for step in range(steps):
            print(f"Step {step}")
            print("Automata:\n", automata.current_grid)
            print("Timer:\n", automata.current_timer_grid, "\n\n")
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_title(f"Step {step}")
            # Create a grid image with colors based on state
            grid_image = [[color_map[state] for state in row] for row in automata.current_grid]
            ax.imshow(grid_image, interpolation='none', aspect='equal')

            # Set aspect of the plot to be equal to ensure square cells
            ax.set_aspect('equal')

            # Adding grid lines
            ax.vlines(np.arange(ncols) - 0.5, ymin=-0.5, ymax=nrows - 0.5, color='white', linewidth=0.5)
            ax.hlines(np.arange(nrows) - 0.5, xmin=-0.5, xmax=ncols - 0.5, color='white', linewidth=0.5)

            # Adding legend inside the plot
            ax.legend(handles=legend_patches, loc='upper right')
            
            # Accommodate for device and no device
            for (i, j), value in np.ndenumerate(automata.device_grid):
                if value == 1:  # If a device is present
                    if(automata.current_grid[i][j] == automata.State.EXPOSED.value):
                        ax.text(j, i, 'D', ha='center', va='center', color='black', fontsize='xx-small', fontweight='bold')
                    else:
                        ax.text(j, i, 'D', ha='center', va='center', color='white', fontsize='xx-small', fontweight='bold')


            # Remove axis ticks
            ax.axis('off')
            # plt.savefig(f'temp_images/step_{step}.png', bbox_inches='tight')
            plt.savefig(os.path.join(temp_image_dir, f'step_{step}.png'), bbox_inches='tight')

            plt.close()
            
            writer.writerow([step,automata.scount,automata.ecount,automata.icount,automata.qcount,
                             automata.rcount,automata.dcount,nrows*ncols,automata.total_infection_count])

            # Update the automata for the next step
            automata.update_grid()

    # Compile images into a video
    with imageio.get_writer(output_path, fps=max(float(steps)/video_length, 1)) as video:
        for step in range(steps):
            # image = imageio.imread(f'temp_images/step_{step}.png')
            image_path = os.path.join(temp_image_dir, f'step_{step}.png')
            image = imageio.imread(image_path)
            video.append_data(image)

    # Clean up temporary images
    for step in range(steps):
        os.remove(os.path.join(temp_image_dir, f'step_{step}.png'))
    os.rmdir(temp_image_dir)

    print(f"Video saved to {output_path}")
    
    # Output a graph of the states over time
    # graph_csv_input = pd.read_csv('data\output\last_run_state_counts.csv', index_col='step')
    graph_csv_input = pd.read_csv(os.path.join('data', 'output', 'last_run_state_counts.csv'), index_col='step')

    plt.figure(figsize=(16,8), dpi=150)
    graph_csv_input['s'].plot(label='SUSCEPTIBLE',c='green')
    graph_csv_input['e'].plot(label='EXPOSED',c='yellow')
    graph_csv_input['i'].plot(label='INFECTED',c='red')
    graph_csv_input['q'].plot(label='QUARANTINED',c='blue')
    graph_csv_input['r'].plot(label='RECOVERED',c='gray')
    graph_csv_input['d'].plot(label='DEAD',c='black')
    graph_csv_input['total_infected'].plot(label='TOTAL INFECTED',c='red',linestyle='dotted')
    plt.title('State Counts Over Time')
    plt.xlabel('Step')
    plt.ylabel('Count')
    plt.legend()


    #plt.savefig('data\output\last_run_state_count_graph.png')
    plt.savefig(os.path.join('data', 'output', 'last_run_state_count_graph.png'))








    # # Device colors from automata
    # device_colors = automata.get_device_colors()
    # d_color_map = {device: mcolors.to_rgba(color) for device, (_, color) in device_colors.items()}
    # d_legend_patches = [mpatches.Patch(color=color, label=label) for _, (label, color) in device_colors.items()]
