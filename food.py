import evolution_switches as es
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
        if es.food_reproduction_threshold:
            new_rep_thresh = reproduction_threshold + randint(-5, 5)
        else:
            new_rep_thresh = 30 + randint(-5, 5)

        if new_rep_thresh < 16:
            new_rep_thresh = 16

        Organism.__init__(self, position, energy, new_rep_thresh, energy_max, gene_val)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += 1
