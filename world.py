import random
import numpy as np
from organism_type import OrganismType
from direction import Direction


class World:
    """
    A class to create in the environment in which our organisms live.
    """
    def __init__(self, time=0, rows=9, columns=10):
        """
        World Initialisation
        :param time: Time at which the world begins to exist
        :param rows: Number of rows in the world
        :param columns: Number of columns in the world
        """
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def random_position(self):
        x = random.randint(0, self.columns - 1)
        y = random.randint(0, self.rows - 1)
        return [x, y]

    def get_disallowed_directions(self, current_position, organism_type):
        "Each organism cannot collide with itself (no overlap)."
        disallowed_directions = []

        if self.check_collision(current_position + np.array([0, 1]), organism_type):
            disallowed_directions.append(Direction.up)
        if self.check_collision(current_position + np.array([0, -1]), organism_type):
            disallowed_directions.append(Direction.down)
        if self.check_collision(current_position + np.array([-1, 0]), organism_type):
            disallowed_directions.append(Direction.left)
        if self.check_collision(current_position + np.array([1, 0]), organism_type):
            disallowed_directions.append(Direction.right)

        return disallowed_directions

    def check_collision(self, position, organism_type):
        "Check if position is out of bounds and for disallowed collisions."
        if position[0] < 0 or position[0] >= self.rows or position[1] < 0 or position[1] >= self.columns:
            return True

        if organism_type == OrganismType.food:
            for food in self.foodList:
                if (position == food.position).all():
                    return True
        elif organism_type == OrganismType.bug:
            for bug in self.bugList:
                if (position == bug.position).all():
                    return True

        return False
