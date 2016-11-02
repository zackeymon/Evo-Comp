import numpy as np


class Organism:
    """
    The parent class for all organisms living in the world.
    """

    def __init__(self, position, lifetime, energy, reproduction_threshold, energy_max):
        """
        Organism Initialisation
        :param position: The current position of the organism in the world
        :param lifetime: The lifetime of the organism
        :param energy: The energy the organism has stored
        :param reproduction_threshold: The energy value at which the organism reproduces
        :param energy_max: The maximum energy the organism can store
        """
        self.position = np.array(position)
        self.lifetime = lifetime
        self.energy = energy
        self.energy_initial = energy
        self.reproduction_threshold = reproduction_threshold
        self.energy_max = energy_max

    def __repr__(self):
        return '%s-[%s, %s]' % (self.__class__.__name__, self.position[0], self.position[1])

    def reproduce(self, direction):
        """"Return new organism from reproduction."""
        self.energy = self.energy_initial

        # Set new parameters
        new_position = self.position + direction
        new_lifetime = 0
        new_energy = self.energy_initial
        new_energy_max = self.energy_max
        new_reproduction_threshold = self.reproduction_threshold

        # Create new object
        return self.__class__(new_position, new_lifetime, new_energy, new_reproduction_threshold, new_energy_max)
