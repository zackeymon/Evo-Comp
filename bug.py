import numpy as np
from organism import Organism


class Bug(Organism):
    def __init__(self, position, energy, reproduction_threshold, energy_max):
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max)

    def respire(self):
        self.energy -= 1

    def eat(self, food, no_of_bugs):
        self.energy += food.energy/no_of_bugs #share food?

    def move(self, del_pos):
        self.position += del_pos

    def reproduce(self, new_pos):
        self.energy = self.energy_initial

        # Set new bug parameters
        new_energy = self.energy_initial
        new_reproduction_threshold = self.reproduction_threshold

        # Create new bug object
        new_bug = Bug(new_pos, new_energy, new_reproduction_threshold)
        return new_bug
