import numpy as np

class Organism:

    def __init__(self, position, energy, reproduction_threshold, energy_max):
        self.position = np.array(position)
        self.energy = energy
        self.energy_initial = energy
        self.reproduction_threshold = reproduction_threshold
        self.energy_max = energy_max

