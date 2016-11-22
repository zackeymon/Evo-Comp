from organism import Organism


class Bug(Organism):
    """
    A class for a simple bug organism that moves, eats, and reproduces.
    """
    def __init__(self, position, energy, reproduction_threshold, energy_max, gene_val):
        """
        Bug Initialisation
        :param position: The current position of the bug in the world
        :param energy: The energy the bug has stored
        :param reproduction_threshold: The energy value at which the bug reproduces
        :param energy_max: The maximum energy the bug can store
        :param gene_val: The gene paramter of the bug
        """
        Organism.__init__(self, position, energy, reproduction_threshold, energy_max, gene_val)

    def respire(self):
        self.energy -= 1

    def eat(self, food):
        # if (self.energy + food.energy) > self.energy_max:
        #     self.energy = self.energy_max
        # else:
        self.energy += food.energy

    def move(self, del_pos):
        self.position += del_pos
