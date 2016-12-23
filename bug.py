from random import randint
import config as cfg
from organism import Organism


class Bug(Organism):
    """
    A class for a simple bug organism that moves, eats, and reproduces.
    """

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

        Organism.__init__(self, position, energy, new_rep_thresh, energy_max, new_taste)

    def respire(self):
        self.energy -= cfg.bug['respiration_rate']

    def eat(self, food):
        self.energy += food.energy

    def move(self, del_pos):
        self.position += del_pos
