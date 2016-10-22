import numpy as np
from direction import Direction


class World:
    def __init__(self, time=0, rows=9, columns=10):
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def check_collision(self, position, plant=False):
        disallowed_directions = []

        if position[1] + 1 >= self.rows:
            disallowed_directions.append(Direction.up)
        if position[1] - 1 < 0:
            disallowed_directions.append(Direction.down)
        if position[0] - 1 < 0:
            disallowed_directions.append(Direction.left)
        if position[0] + 1 >= self.columns:
            disallowed_directions.append(Direction.right)

        if plant:
            for food in self.foodList:
                if position + np.array([0, 1]) == food.position:
                    disallowed_directions.append(Direction.up)
                if position + np.array([0, -1]) == food.position:
                    disallowed_directions.append(Direction.down)
                if position + np.array([-1, 0]) == food.position:
                    disallowed_directions.append(Direction.left)
                if position + np.array([1, 0]) == food.position:
                    disallowed_directions.append(Direction.right)

        list(set(disallowed_directions))
        return disallowed_directions
