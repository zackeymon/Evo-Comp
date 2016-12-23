import numpy as np
from random import randint


class Organism:
    """
    The parent class for all organisms living in the world.
    """

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
        self.reproduction_threshold = reproduction_threshold
        self.energy_max = energy_max
        self.taste = taste

        if self.reproduction_threshold < 2:
            self.reproduction_threshold = 2

    def __repr__(self):
        return '%s(P:[%d, %d] L:%d E:%d RT:%d E_max:%d g:%d)' % (
            self.__class__.__name__, self.position[0], self.position[1], self.lifetime, self.energy,
            self.reproduction_threshold, self.energy_max, self.taste)

    @staticmethod
    def mutate(current_val, max_mutation_rate):
        return current_val + randint(-max_mutation_rate, max_mutation_rate)

    def reproduce(self, direction):
        """"Return new organism from reproduction."""
        # Half of the energy goes to the offspring
        self.energy = int(self.energy / 2)

        # Set new parameters
        new_position = self.position + direction
        new_energy = self.energy
        new_energy_max = self.energy_max
        new_reproduction_threshold = self.reproduction_threshold
        new_taste = self.taste

        # Create new object
        return self.__class__(new_position, new_energy, new_reproduction_threshold, new_energy_max, new_taste)
