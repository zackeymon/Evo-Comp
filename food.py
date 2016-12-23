from random import randint
import config as cfg
from organism import Organism


class Food(Organism):
    """
    A class for a food organism that simply grows and sustains life.
    """
    def __init__(self, position, energy, reproduction_threshold, energy_max, taste):
        """
        Food Initialisation
        :param position: The current position of the food in the world
        :param energy: The energy stored in the food
        :param reproduction_threshold: The energy value at which the food reproduces
        :param energy_max: The maximum energy the food can hold
        :param taste: The gene parameter of the food
        """
        new_rep_thresh = self.mutate(reproduction_threshold, cfg.food['reproduction_threshold_mutation_limit']) \
            if cfg.food['evolve_reproduction_threshold'] else 30 + randint(-5, 5)

        new_taste = self.mutate(taste, cfg.food['taste_mutation_limit']) if cfg.food['evolve_taste'] else taste

        if new_rep_thresh < 10:
            new_rep_thresh = 10

        # ToDo: Food Die

        Organism.__init__(self, position, energy, new_rep_thresh, energy_max, new_taste)

    def grow(self):
        if self.energy < self.energy_max:
            self.energy += cfg.food['growth_rate']
