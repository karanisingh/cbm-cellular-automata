# src/models/SEIQRD1ProbabilisticCellularAutomata.py

from enum import Enum
import numpy as np
from ..utils.neighborhood import get_neighbors_moore as get_neighbors
from .CellularAutomata import CellularAutomata


# SEIQRD 1
# This model works with 6 states: Susceptible, Exposed, Quarantined, Infected, Recovered, Dead
# Grid passed should have values ranging from 0-5
# Transition:
#   P(S --> E)      --> P(Exposure)*(#exposed_moore + #infected_moore)
#                    -> Transition delay = 0 (instantaneous exposure)
#                    -> Moore neighboorhood, with d=1
#
#   P(E --> I)      --> P(Infection | Exposure) = prob infection grows and shows symptoms
#                    -> Transition delay = 8 (incubation period)
#
#   P(E --> S)      --> P(!Infection | Exposure) = prob that infection is not developed
#                    -> Transition delay = 8 (incubation period)
#
#   P(I --> Q)      --> P(Quarantine) = measures efficiency of testing methods
#                    -> Transition delay = measures promptness of testing
#
#   P({I, Q} --> R) --> P(Recover) = measure efficiency of healthcare and wellness of pop
#                    -> Transition delay = 14 (2 weeks to recover)
#
#   P({I, Q} --> D) --> P(Death) = measure inefficiency of healthcare and unwellness of pop
#                    -> Transition delay = 5 (1 week for disease to become fatal)
#                    -> Transition cutoff = 8
#
#   exposure_prob   = probability that you are exposed given n exposed and m infected neighbors
#   infection_prob  = probability that infection occurs after exposure_delay
#   quarantine_prob = probability that infected becomes quarantined after 5 days of testing/results
#   recovery_prob   = probability that someone recovers after 14 days of initial Infection
#

class SEIQRD1ProbabilisticCellularAutomata(CellularAutomata):

    # 6 STATES
    class State(Enum):
        SUSCEPTIBLE = 0
        EXPOSED = 1
        INFECTED = 2
        QUARANTINED = 3
        RECOVERED = 4
        DEAD = 5

    def __init__(self, grid, exposure_prob, infection_prob, quarantine_prob, recovery_prob, death_prob):
        # Grids
        super().__init__(grid)
        self.current_timer_grid = np.zeros_like(grid)

        # Constants needed
        self.exposure_prob = exposure_prob
        self.infection_prob = infection_prob
        self.quarantine_prob = quarantine_prob
        self.recovery_prob = recovery_prob
        self.death_prob = death_prob
        self.infection_delay = 8                    # According to research paper
        self.quarantine_delay = 4                   # ASSUME: Testing takes 1 day, results take 2 days, quarantine takes 1 day
        self.recovery_delay = 14                    # ASSUME: Disease course takes 2 weeks
        self.death_delay = 5                        # ASSUME: Disease takes 1 week to become fatal
        self.death_cutoff = 8
        self.moore_d = 1                            # Radius of moore neighborhood
        self.rng = np.random.default_rng()

        # Needed to determine termination 
        self.sameStateCount = 0

    def update_cell(self, x, y):
        # Get current cell's state and Moore neighborhood)
        state = self.State(self.current_grid[x, y])
        neighborhood = get_neighbors(self.current_grid, x, y)
        num_infected_neighbors = 0
        num_exposed_neighbors = 0
        for neighbor in neighborhood:
            if self.State(neighbor) == self.State.INFECTED:
                num_infected_neighbors += 1
            elif self.State(neighbor) == self.State.EXPOSED:
                num_exposed_neighbors += 1

        # Get current cell's timer
        timer = self.current_timer_grid[x, y]

        ##############
        # Transition #
        ##############

        # P(S --> E) = P(exposure)*(#exposed_moore + #infected_moore)
        if state == self.State.SUSCEPTIBLE and num_infected_neighbors > 0:
            if self.rng.random() < self.exposure_prob * (num_infected_neighbors + num_exposed_neighbors):
                return (self.State.EXPOSED.value, 1)  # Start exposure timer
        
        # P(E --> {S, I})
        elif state == self.State.EXPOSED:
            if timer >= self.infection_delay:
                # P(E --> I) = P(Infection) | infection_delay
                if self.rng.random() < self.infection_prob:
                    return (self.State.INFECTED.value, 1)  # Start infection timer
                # P(E --> S) = !P(E --> I) | infection delay
                else:
                    return (self.State.SUSCEPTIBLE.value, 1) # Start susceptible timer (not used)

        # P(I --> {R, D, Q})
        elif state == self.State.INFECTED:
            # P(I --> R) = P(100%) | Recovery_delay
            if timer >= self.recovery_delay and self.rng.random() < self.recovery_prob:
                return (self.State.RECOVERED.value, 0)

            # P(I --> D) = P(Death) | 7 days is peak for deth
            if timer >= self.death_delay and timer <= self.death_cutoff and self.rng.random() < self.death_prob:
                return (self.State.DEAD.value, 0)

            # P(I --> Q) = P(Quarantine) | Quarantine_delay
            if timer >= self.quarantine_delay and self.rng.random() < self.quarantine_prob:
                return (self.State.QUARANTINED.value, timer)  # Continue quarantine timer from infection timer
  
        # P(Q --> {R, D})
        elif state == self.State.QUARANTINED:
            # P(Q --> R) = P(100%) | Recovery_delay
            if timer >= self.recovery_delay and self.rng.random() < self.recovery_prob:
                return (self.State.RECOVERED.value, 0)

            # P(Q --> D) = P(Death) | 7 days is peak for deth
            if timer >= self.death_delay and timer <= self.death_cutoff and self.rng.random() < self.death_prob:
                return (self.State.DEAD.value, 0)

        # Increment timer if state has not changed
        # if state == self.current_grid[x, y]:
        #    self.timer_grid[x, y] += 1

        return (state.value, self.current_timer_grid[x, y]+1)

    def update_grid(self):
        next_grid = np.copy(self.current_grid)
        next_timer_grid = np.copy(self.current_timer_grid)

        for x in range(self.current_grid.shape[0]):
            for y in range(self.current_grid.shape[1]):
                next_state, next_timer = self.update_cell(x, y)
                next_grid[x, y] = next_state
                next_timer_grid[x, y] = next_timer

        # TODO: Termination

        self.current_grid = next_grid
        self.current_timer_grid = next_timer_grid

    def get_state_colors(self):
        return {
            self.State.SUSCEPTIBLE.value: ("SUSCEPTIBLE", "green"),
            self.State.EXPOSED.value: ("EXPOSED", "yellow"),
            self.State.INFECTED.value: ("INFECTED", "red"),
            self.State.QUARANTINED.value: ("QUARANTINED", "blue"),
            self.State.RECOVERED.value: ("RECOVERED", "gray"),
            self.State.DEAD.value: ("DEAD", "black")
        }


