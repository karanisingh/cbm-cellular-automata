## Main hook

import argparse
import numpy as np
from .utils.visualize import visualize_automata, save_final_state
from .utils.create_grid import create_grid_from_file
from .models.basic_cellular_automata import BasicCellularAutomata


def main(args):
    # get the location of the input board, and where to store the output board
    input_path = args.input_path
    output_path = args.output_path

    # get the initial parameters for the model
    #grid_size = args.grid_size
    num_steps = args.num_steps

    # others
    visualize = args.visualize
    debug = args.debug

    if debug:
        print(f"Input path \t--> {input_path}")
        print(f"Output path \t--> {output_path}")
        print(f"Number of steps --> {num_steps}")
        print(f"Visualize \t--> {visualize}")
        print(f"Debug \t\t--> {debug}")

    # Process the input data
    grid = create_grid_from_file(input_path)
    if debug:
        print("Initial grid:\n")
        print(grid)


    # Create the cellular automata model based on initial grid
    automata = BasicCellularAutomata(grid)
    if debug:
        print("Automata created")


    if debug:
        print("Running the cellular automata model...")
        
    # Run the cellular automata model
    if visualize:
        visualize_automata(automata, num_steps, output_path)
    else:
        for _ in range(num_steps):
            automata.update_grid()
        save_final_state(automata, output_path)
        

    if debug:
        print("Done!")
    return

