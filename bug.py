import numpy as np
from direction import Direction

class Bug:

    def __init__(self, pos, energy, reproduction_threshold):
        self.pos = np.array(pos)
        self.energy = energy
        self.energy_initial = energy
        self.reproduction_threshold = reproduction_threshold
        # self.energy_max = energy_max

    def respire(self):
        self.energy -= 1

    def eat(self, food):
        self.energy += food.energy

    def move(self, del_pos):
        self.pos += del_pos

    def reproduce(self, new_pos):
        self.energy = self.energy_initial

        # Set new bug parameters
        new_energy = self.energy_initial
        new_reproduction_threshold = self.reproduction_threshold

        # Create new bug object
        new_bug = Bug(new_pos, new_energy, new_reproduction_threshold)
        return new_bug
