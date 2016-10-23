import numpy as np
from organism import Organism


class Food(Organism):
    def __init__(self, position, energy, reproduction_threshold, energy_max):
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += 1

    def reproduce(self, new_pos):
        self.energy = self.energy_initial

        # Set the parameters for the new food
        new_energy = self.energy_initial
        new_reproduction_threshold = self.reproduction_threshold
        new_energy_max = self.energy_max

        # Create new food object
        new_food = Food(new_pos, new_energy, new_reproduction_threshold, new_energy_max)
        return new_food
