import numpy as np
from organism import Organism


class Bug(Organism):
    def __init__(self, position, energy=30, reproduction_threshold=70, energy_max=100):
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max)

    def respire(self):
        self.energy -= 1

    def eat(self, food):
        if (self.energy + food.energy) > self.energy_max:
            self.energy = self.energy_max
        else:
            self.energy += food.energy

    def move(self, del_pos):
        self.position += del_pos
