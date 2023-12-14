# src/models/SEIQRD_DevicePCA.py

from enum import Enum
import numpy as np
from ..utils.neighborhood import get_neighbors_moore as get_neighbors
from .CellularAutomata import CellularAutomata

############################################################################################################
#
# SEIQRD Device
#
# This model works with 2 Grids: State Layer (dynamic) and Device Layer (static)
#
############################################################################################################
#
# State Layer:
#
# Grid with values to state mapping as such:
#   0 = Susceptible
#   1 = Exposed
#   2 = Infected
#   3 = Quarantined
#   4 = Recovered
#   5 = Dead
#
# This model works with 6 states: Susceptible, Exposed, Quarantined, Infected, Recovered, Dead
# 
# Transition:
#   P(S --> E | !Device)     --> P(Exposure)*(#exposed_moore + #infected_moore)
#                            -> Transition delay = 0 (instantaneous exposure)
#                            -> Moore neighboorhood, with d=1
#
#   P(S --> E | Device)    --> (P(Exposure)*device_pm1)*(#exposed_moore + #infected_moore)
#                            -> Transition delay = 0 (instantaneous exposure)
#                            -> Moore neighboorhood, with d=1
#
#   P(E --> I)      --> P(Infection | Exposure) = prob infection grows and shows symptoms
#                    -> Transition delay = 8 (incubation period)
#
#   P(E --> S)      --> P(!Infection | Exposure) = prob that infection is not developed
#                    -> Transition delay = 8 (incubation period)
#
#   P(I --> Q | !Device)    --> P(Quarantine) = measures efficiency of testing methods
#                            -> Transition delay = 4 (measures promptness of testing)
#
#   P(I --> Q | Device)     --> P(Quarantine) = measures efficiency of testing methods
#                            -> Transition delay = 4 - device_pm2 (measures promptness of testing)
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
#   device_pm1      = real number \in (0-1] 
#                     This parameter is multiplied to the probability of exposure
#                     to accommodate for the device being able to better notify
#                     folks of chance of being exposed, and so decreases probability
#                     of exposure. 
#                     
#                     IRL = device gives you info if others around you are exposed, so 
#                           you can (hopefully) try to stay cautious, and thus decrease
#                           probability you are exposed
#
#   device_pm2      = integer \in [0, quarantine_delay)
#                     This parameter is subtracted to the quarantine_delay time
#                     to accommodate for the device being able to better notify
#                     users of if they are infected or not, and therefore decreases
#                     the time it takes to test and quarantine oneself
#
#                     IRL = device has included at home testing kit in it or something
#                       
#                                  
#
###########################################################################################################
#
# Device Layer:
#
# Grid with values to device mapping as such:
#   0 = No Device
#   1 = Has Device
#
###########################################################################################################
class SEIQRD_DevicePCA(CellularAutomata):

    # 6 State States
    class State(Enum):
        SUSCEPTIBLE = 0
        EXPOSED = 1
        INFECTED = 2
        QUARANTINED = 3
        RECOVERED = 4
        DEAD = 5

    # 2 Device States
    class Device(Enum):
        NO_DEVICE = 0
        HAS_DEVICE = 1   

    

    def __init__(self, grid, device_grid, exposure_prob, infection_prob, quarantine_prob, recovery_prob, death_prob, device_pm1, device_pm2):
        # Grids
        super().__init__(grid)
        self.current_timer_grid = np.zeros_like(grid)
        self.device_grid = np.copy(device_grid)

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

        self.device_pm1 = device_pm1
        self.device_pm2 = device_pm2

        # Needed to determine termination 
        self.sameStateCount = 0
        
        # Number of cells in each state
        self.total_infection_count = 0
        self.scount = 0
        self.ecount = 0
        self.icount = 0
        self.qcount = 0
        self.rcount = 0
        self.dcount = 0
        for cell in grid.flat:
            match cell:
                case 0:
                    self.scount += 1
                case 1:
                    self.ecount += 1
                case 2:
                    self.icount += 1
                    self.total_infection_count += 1
                case 3:
                    self.qcount += 1
                case 4:
                    self.rcount += 1
                case 5:
                    self.dcount += 1
        

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
        device = self.device_grid[x, y]

        
        ###############
        # Transition  #
        ###############

        # P(S --> E) = P(exposure)*(#exposed_moore + #infected_moore)
        if state == self.State.SUSCEPTIBLE and num_infected_neighbors > 0:
            #   P(S --> E | !Device)
            if not device and self.rng.random() < self.exposure_prob * (num_infected_neighbors + num_exposed_neighbors):
                return (self.State.EXPOSED.value, 1)  # Start exposure timer
             #   P(S --> E | Device)
            elif device and self.rng.random() < (self.exposure_prob*self.device_pm1) * (num_infected_neighbors + num_exposed_neighbors):
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

            # P(I --> Q | !Device)
            if not device and timer >= self.quarantine_delay and self.rng.random() < self.quarantine_prob:
                return (self.State.QUARANTINED.value, timer)  # Continue quarantine timer from infection timer
            elif device and timer >= self.quarantine_delay - self.device_pm2 and self.rng.random() < self.quarantine_prob:
                return (self.State.QUARANTINED.value, timer)  # Continue quarantine timer
  
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
        
        # reset state counts to 0
        self.scount = 0
        self.ecount = 0
        self.icount = 0
        self.qcount = 0
        self.rcount = 0
        self.dcount = 0

        for x in range(self.current_grid.shape[0]):
            for y in range(self.current_grid.shape[1]):
                next_state, next_timer = self.update_cell(x, y)
                next_grid[x, y] = next_state
                next_timer_grid[x, y] = next_timer
                match next_state:
                    case 0:
                        self.scount += 1
                    case 1:
                        self.ecount += 1
                    case 2:
                        self.icount += 1
                        if (self.current_grid[x, y] < 2):
                            self.total_infection_count += 1
                    case 3:
                        self.qcount += 1
                    case 4:
                        self.rcount += 1
                    case 5:
                        self.dcount += 1

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

    def get_device_colors(self):
        return {
            self.Device.NO_DEVICE.value: ("NO DEVICE", "red"),
            self.Device.DEVICE.value: ("DEVICE", "green")
        }

