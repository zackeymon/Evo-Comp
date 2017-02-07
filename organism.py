import numpy as np
from random import randint


class Organism:
    """
    The parent class for all organisms living in the world.
    """
    reproduction_cost = None
    maturity_age = None

    def __init__(self, position, energy, reproduction_threshold, energy_max, taste):
        """
        Organism Initialisation
        :param position: The current position of the organism in the world
        :param energy: The energy the organism has stored
        :param reproduction_threshold: The energy value at which the organism reproduces
        :param energy_max: The maximum energy the organism can store
        :param taste: The gene parameter of the organism
        """
        self.position = np.array(position)
        self.lifetime = 0
        self.energy = energy
        self.reproduction_threshold = reproduction_threshold if reproduction_threshold >= 0 else 0  # <0 is unphysical
        self.energy_max = energy_max
        self.taste = taste % 360
        self.offspring_energy_fraction = 0.4

    def __repr__(self):
        return '%s(P:[%d, %d] L:%d E:%d RT:%d E_max:%d g:%d)' % (
            self.__class__.__name__, self.position[0], self.position[1], self.lifetime, self.energy,
            self.reproduction_threshold, self.energy_max, self.taste)

    @staticmethod
    def mutate(current_val, max_mutation_rate):
        return current_val + randint(-max_mutation_rate, max_mutation_rate)

    def can_reproduce(self):
        return self.energy >= self.reproduction_threshold and self.lifetime > self.maturity_age

    def reproduce(self, direction):
        """"Return new organism from reproduction."""
        # Set new parameters
        new_position = self.position + direction
        new_energy = int(self.energy * self.offspring_energy_fraction)
        new_energy_max = self.energy_max
        new_reproduction_threshold = self.reproduction_threshold
        new_taste = self.taste

        # Loses that much energy
        self.energy -= (new_energy + self.reproduction_cost)
        if self.energy < 0:
            self.energy = 0

        # Create new object
        return self.__class__(new_position, new_energy, new_reproduction_threshold, new_energy_max, new_taste)
