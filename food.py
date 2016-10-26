import numpy as np
from organism import Organism


class Food(Organism):
    def __init__(self, position, energy=20, reproduction_threshold=70, energy_max=100):
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += 1
