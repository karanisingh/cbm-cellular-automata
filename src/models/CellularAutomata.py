# src/models/CellularAutomata.py

from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class CellularAutomata(ABC):

    def __init__(self, grid):
        self.original_grid = np.copy(grid)
        self.current_grid = np.copy(grid)

    @abstractmethod
    def update_cell(self, x, y):
        pass

    @abstractmethod
    def update_grid(self):
        pass

    @abstractmethod
    def get_state_colors(self):
        pass
