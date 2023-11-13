# src/models/basic_cellular_automata.py
# first time testing cellular automata

import numpy as np
from enum import Enum
from ..utils.neighborhood import get_neighbors_von_neumann as get_neighbors


# This model works with 2 states: infected, susceptible
# Grid passed should only have 0 (susceptible) and 1 (infected) as states for initial board 
# Transition: if anyone in Von Neumann neighborhood is infected, you become infected
class BasicCellularAutomata:

    class State(Enum):
        SUSCEPTIBLE = 0
        INFECTED = 1

    def __init__(self, grid):
        self.original_grid = np.copy(grid)
        self.current_grid = np.copy(grid)

    # update the state of the current cell based on the transition rules
    def update_cell(self, x, y):
        # if we are infected we stay infected
        if self.current_grid[x, y] == self.State.INFECTED.value:
            return self.State.INFECTED.value

        # get the neighorhood, see if anyone is infected
        neighborhood = get_neighbors(self.current_grid, x, y)
        
        # TODO: why the fuck does this not work
        # if np.any(neighborhood == self.State.INFECTED.value):
        #     print("HASDHASD")
        #     return self.State.INFECTED.value
        for neighbor in neighborhood:
            if neighbor == self.State.INFECTED.value:
                return self.State.INFECTED.value

        # no infected neighbors, we stay susceptible    
        return self.State.SUSCEPTIBLE.value



    # do the next step of the cellular automata
    def update_grid(self):
        # next step of grid
        next_grid = np.copy(self.current_grid)

        # iterate through all cells, update cells based on transition
        for x in range(self.current_grid.shape[0]):
            for y in range(self.current_grid.shape[1]):
                next_grid[x, y] = self.update_cell(x, y)
            
        # update the current grid with the one we just calculated
        self.current_grid = next_grid
        
        

