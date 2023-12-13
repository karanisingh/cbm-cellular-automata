# src/main.py

import argparse
import numpy as np
from .utils.runner import visual_runner
from .utils.create_grid import create_grid_from_file
from .models.BasicCellularAutomata import BasicCellularAutomata
from .models.BasicProbabilisticCellularAutomata import BasicProbabilisticCellularAutomata
from .models.SEIQRD1ProbabilisticCellularAutomata import SEIQRD1ProbabilisticCellularAutomata
from .models.SEIQRD_DevicePCA import SEIQRD_DevicePCA

def main(args):
    #####################
    ## Parse arguments ##
    #####################
    input_path = args.input_path
    device_input_path = args.device_input_path
    output_path = args.output_path
    device_param1 = args.device_param1
    device_param2 = args.device_param2
    num_steps = args.num_steps
    record = args.record
    video_length = args.video_length
    debug = args.debug


    if debug:
        print(f"Input grid path \t--> {input_path}")
        print(f"Input DEVICE grid path--> {device_input_path}")
        print(f"Output grid path \t--> {output_path}")
        print(f"Device Parameter 1\t--> {device_param1}")
        print(f"Device Parameter 2\t--> {device_param2}")
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

    # Create the device grid
    d_grid = create_grid_from_file(device_input_path)
    if debug:
        print("Device grid:\n")
        print(d_grid)
    
    automata = SEIQRD_DevicePCA(grid, d_grid, exposure_prob=0.2, infection_prob=0.5, quarantine_prob=0.5, recovery_prob=0.9, death_prob=0.01, device_pm1=device_param1, device_pm2=device_param2)
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

