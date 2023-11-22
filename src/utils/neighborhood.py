# src/utils/neighborhood.py
# functions for getting neighborhoods of a cell
import numpy as np

'''
Given a 2D grid, returns a list of the Von-Neumann neighbors
specified by (x, y)
'''
def get_neighbors_von_neumann(grid, x, y):
    rows, cols = grid.shape
    neighbors = []

    # Define potential neighbor positions
    potential_neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    # Filter out-of-bound positions
    for nx, ny in potential_neighbors:
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append(grid[nx, ny])

    return neighbors

'''
Given a 2D grid, returns a list of the Moore neighbors
specified by (x, y)
'''
def get_neighbors_moore(grid, x, y):
    rows, cols = grid.shape
    neighbors = []

    # Define potential neighbor positions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append(grid[nx, ny])

    return neighbors

