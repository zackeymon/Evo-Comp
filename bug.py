import numpy as np
from organism import Organism


class Bug(Organism):
    def __init__(self, position, energy, reproduction_threshold, energy_max):
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max)

    def respire(self):
        self.energy -= 1

    def eat(self, food, no_of_bugs):
        self.energy += food.energy / no_of_bugs  # share food?

    def move(self, del_pos):
        self.position += del_pos


