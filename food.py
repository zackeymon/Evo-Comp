import config as cfg
from constants import FOOD_VAL, FOOD_NAME
from organism import Organism


class Food(Organism):
    """
    A class for a food organism that simply grows and sustains life.
    """
    value = FOOD_VAL
    name = FOOD_NAME
    reproduction_cost = cfg.food_reproduction_cost

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
            if cfg.food['evolve_reproduction_threshold'] \
            else self.mutate(cfg.world['food_spawn_vals']['reproduction_threshold'], 5)

        new_taste = self.mutate(taste, cfg.food['taste_mutation_limit']) if cfg.food['evolve_taste'] else taste

        Organism.__init__(self, position, energy, new_rep_thresh, energy_max, new_taste)

    def grow(self):
        self.lifetime += 1
        if self.energy < self.energy_max:
            self.energy += cfg.food['growth_rate']

    def can_overshadow(self, defending_plant):
        if self.energy * self.offspring_energy_fraction * cfg.food_over_shadow_ratio > defending_plant.energy:
            return True
