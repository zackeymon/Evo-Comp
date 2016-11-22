import numpy as np
from random import randint


class Organism:
    """
    The parent class for all organisms living in the world.
    """
    def __init__(self, position, energy, reproduction_threshold, energy_max, gene_val):
        """
        Organism Initialisation
        :param position: The current position of the organism in the world
        :param energy: The energy the organism has stored
        :param reproduction_threshold: The energy value at which the organism reproduces
        :param energy_max: The maximum energy the organism can store
        :param gene_val: The gene parameter of the organism
        """
        self.position = np.array(position)
        self.lifetime = 0
        self.energy = energy
        self.reproduction_threshold = reproduction_threshold #+ randint(-5, 5)  # TODO: Evolution 1 switch
        self.energy_max = energy_max
        self.gene_val = gene_val
        if self.reproduction_threshold > energy_max:
            self.reproduction_threshold = self.energy_max

    def __repr__(self):
        return '%s(P:[%d, %d] L:%d E:%d RT:%d Emax:%d)' % (
            self.__class__.__name__, self.position[0], self.position[1], self.lifetime, self.energy,
            self.reproduction_threshold, self.energy_max)

    def reproduce(self, direction):
        """"Return new organism from reproduction."""
        # Half of the energy goes to the offspring
        self.energy = int(self.energy / 2)

        # Set new parameters
        new_position = self.position + direction
        new_energy = self.energy
        new_energy_max = self.energy_max
        new_reproduction_threshold = self.reproduction_threshold

        # Create new object
        return self.__class__(new_position, new_energy, new_reproduction_threshold, new_energy_max)
