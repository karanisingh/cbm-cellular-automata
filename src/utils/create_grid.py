# src/utils/create_grid.py

import numpy as np

def create_grid_from_file(file_path):
    with open(file_path, 'r') as file:
        # Read lines and strip newline characters
        lines = file.readlines()
        
        # Convert each line to a list of integers
        grid_data = [list(map(int, line.strip().split(', '))) for line in lines]

        # Convert the list of lists to a NumPy array
        grid = np.array(grid_data)

    return grid
