# src/models/BasicCellularAutomata.py

import numpy as np
from enum import Enum
from ..utils.neighborhood import get_neighbors_von_neumann as get_neighbors
from .CellularAutomata import CellularAutomata

# This model works with 2 states: infected, susceptible
# Grid passed should only have 0 (susceptible) and 1 (infected) as states for initial board 
# Transition: if anyone in Von Neumann neighborhood is infected, you become infected
'''
Our first Cellular Automata Model
'''
class BasicCellularAutomata(CellularAutomata):

    class State(Enum):
        SUSCEPTIBLE = 0
        INFECTED = 1

    # update the state of the current cell based on the transition rules
    def update_cell(self, x, y):
        # if we are infected we stay infected
        if self.current_grid[x, y] == self.State.INFECTED.value:
            return self.State.INFECTED.value

        # get the neighorhood, see if anyone is infected
        neighborhood = get_neighbors(self.current_grid, x, y)
        for neighbor in neighborhood:
            if neighbor == self.State.INFECTED.value:
                return self.State.INFECTED.value

        # no infected neighbors, we stay susceptible    
        return self.State.SUSCEPTIBLE.value



    # do the next step of the cellular automata
    def update_grid(self):
        # Check if we have reached the termination condition
        if self.is_terminated:
            print("\n\n\nTERMINATED\n\n")
            return

        # next step of grid
        next_grid = np.copy(self.current_grid)

        

        # iterate through all cells, update cells based on transition
        cum_state = 0
        for x in range(self.current_grid.shape[0]):
            for y in range(self.current_grid.shape[1]):
                next_grid[x, y] = self.update_cell(x, y)
                cum_state += next_grid[x, y]

        # See if we are in a terminating state
        if cum_state == self.current_grid.shape[0]*self.current_grid.shape[1]:
            self.is_terminated = True
            
        # update the current grid with the one we just calculated
        self.current_grid = next_grid
        
    # Get the state map for this automata model
    # state.value --> (state.name, state.color)
    # colors must be compatible with mcolor.ListedColormap
    def get_state_colors(self):
        return {
            0: ("SUSCEPTIBLE", "green"),
            1: ("INFECTED", "red")
        }



        

