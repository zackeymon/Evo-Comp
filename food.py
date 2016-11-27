from random import randint
from organism import Organism


class Food(Organism):
    """
    A class for a food organism that simply grows and sustains life.
    """
    def __init__(self, position, energy, reproduction_threshold, energy_max, gene_val):
        """
        Food Initialisation
        :param position: The current position of the food in the world
        :param energy: The energy stored in the food
        :param reproduction_threshold: The energy value at which the food reproduces
        :param energy_max: The maximum energy the food can hold
        :param gene_val: The gene parameter of the food
        """
        Organism.__init__(self, position, energy, 30 + randint(-5, 5), energy_max)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += 1
