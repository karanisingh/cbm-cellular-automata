# src/main.py

import argparse
import numpy as np
from .utils.runner import visual_runner
from .utils.create_grid import create_grid_from_file
from .models.BasicCellularAutomata import BasicCellularAutomata


def main(args):
    #####################
    ## Parse arguments ##
    #####################
    input_path = args.input_path
    output_path = args.output_path
    num_steps = args.num_steps
    record = args.record
    video_length = args.video_length
    debug = args.debug


    if debug:
        print(f"Input path \t--> {input_path}")
        print(f"Output path \t--> {output_path}")
        print(f"Number of steps --> {num_steps}")
        print(f"Record \t--> {record}")
        print(f"Video length    --> {video_length}")
        print(f"Debug \t\t--> {debug}")

    ##############################################################
    ## Create the cellular automata model based on initial grid ##
    ##############################################################
    
    # Process the input data
    grid = create_grid_from_file(input_path)
    if debug:
        print("Initial grid:\n")
        print(grid)
    
    automata = BasicCellularAutomata(grid)
    if debug:
        print("Automata created")

        
    #####################################
    ## Run the cellular automata model ##
    #####################################
    if debug:
        print("Running the cellular automata model...\n----------------------------------------------------\n\n")

    
    visual_runner(automata, num_steps, output_path, record, video_length)
        
    if debug:
        print("Done!")
    return

