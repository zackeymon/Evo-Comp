from organism import Organism
from random import randint


class Food(Organism):
    """
    A class for a food organism that simply grows and sustains life.
    """
    def __init__(self, position, lifetime=0, energy=20 + randint(-5, 5), reproduction_threshold=30, energy_max=100):
        """
        Food Initialisation
        :param position: The current position of the food in the world
        :param lifetime: The lifetime of the food
        :param energy: The energy stored in the food
        :param reproduction_threshold: The energy value at which the food reproduces
        :param energy_max: The maximum energy the food can hold
        """
        Organism.__init__(self, position, lifetime, energy, reproduction_threshold, energy_max)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += 1
