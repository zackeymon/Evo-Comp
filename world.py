import numpy as np
from organism_type import OrganismType
from direction import Direction


class World:
    def __init__(self, time=0, rows=9, columns=10):
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def get_disallowed_directions(self, current_position, organism_type):
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
        # Check if the position is out of bound
        if position[0] < 0 or position[0] >= self.rows or position[1] < 0 or position[1] >= self.columns:
            return True

        if organism_type == OrganismType.food:
            for food in self.foodList:
                if position == food.position:
                    return True
        elif organism_type == OrganismType.bug:
            for bug in self.bugList:
                if position == bug.position:
                    return True

        return False
