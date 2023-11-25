# src/models/BasicProbabilisticCellularAutomata.py

import numpy as np
from enum import Enum
from ..utils.neighborhood import get_neighbors_von_neumann as get_neighbors
from .CellularAutomata import CellularAutomata

# This model works with 2 states: infected, susceptible
# Grid passed should only have 0 (susceptible) and 1 (infected) as states for initial board 
# Transition: If ANYONE in von-neuman neighborhood is infected, you have a 50% chance of being infected
'''
Our first Cellular Automata Model
'''
class BasicProbabilisticCellularAutomata(CellularAutomata):

    class State(Enum):
        SUSCEPTIBLE = 0
        INFECTED = 1

    def __init__(self, grid):
        self.rng = np.random.default_rng()

        # Superclass
        super().__init__(grid)

    # update the state of the current cell based on the transition rules
    def update_cell(self, x, y):
        # if we are infected we stay infected
        if self.current_grid[x, y] == self.State.INFECTED.value:
            return self.State.INFECTED.value

        # get the neighorhood, see if anyone is infected
        neighborhood = get_neighbors(self.current_grid, x, y)
        
        # TODO: why the FUCK does this not work
        # if np.any(neighborhood == self.State.INFECTED.value):
        #     print("HASDHASD")
        #     return self.State.INFECTED.value

        # Check if anyone is infected in the von_neuman neighborhood
        infected_neighbor = False
        for neighbor in neighborhood:
            if neighbor == self.State.INFECTED.value:
                # If someone is infected, let's see 50% chance of getting infected
                if self.rng.random() > 0.5:
                    return self.State.INFECTED.value
                else:
                    return self.State.SUSCEPTIBLE.value

        # no infected neighbors, we stay susceptible    
        return self.State.SUSCEPTIBLE.value



    # do the next step of the cellular automata
    def update_grid(self):
        # Check if we have reached the termination condition
        if self.is_terminated:
            print("\n\n\nTERMINATED\n\n\n")
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

    # This model will terminate when all cells infected
    # def is_terminated(self):
    #     for x in range(self.current_grid.shape[0]):
    #         for y in range(self.current_grid.shape[1]):
    #             if current_grid[x, y] == self.State.SUSCEPTIBLE.value:
    #                 return False
    #     return True

        

