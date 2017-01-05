import numpy as np
import config as cfg
from random import randint
from constants import BUG_VAL, BUG_NAME
from utility_methods import get_taste_average
from organism import Organism


class Bug(Organism):
    """
    A class for a simple bug organism that moves, eats, and reproduces.
    """
    value = BUG_VAL
    name = BUG_NAME

    def __init__(self, position, energy, reproduction_threshold, energy_max, taste):
        """
        Bug Initialisation
        :param position: The current position of the bug in the world
        :param energy: The energy the bug has stored
        :param reproduction_threshold: The energy value at which the bug reproduces
        :param energy_max: The maximum energy the bug can store
        :param taste: The gene parameter of the bug
        """
        new_rep_thresh = self.mutate(reproduction_threshold, cfg.bug['reproduction_threshold_mutation_limit']) \
            if cfg.bug['evolve_reproduction_threshold'] else reproduction_threshold

        new_taste = self.mutate(taste, cfg.bug['taste_mutation_limit']) if cfg.bug['evolve_taste'] else taste

        self.mouth_size = 30

        Organism.__init__(self, position, energy, new_rep_thresh, energy_max, new_taste)

    def respire(self):
        self.lifetime += 1
        self.energy -= cfg.bug['respiration_rate']

    def eat(self, food):
        """Take a bite, if ate the whole food return True, else return False"""
        if self.mouth_size >= food.energy:
            self.energy += food.energy
            return True

        self.energy += self.mouth_size
        food.energy -= self.mouth_size
        return False

    def move(self, del_pos):
        self.position += del_pos

    def try_eat(self, food):
        self.energy -= cfg.bug['eat_tax']
        if np.absolute(self.taste - get_taste_average([self.taste, food.taste])) <= randint(0, 180):  # eating chance
            if self.eat(food):
                return True
        return False
