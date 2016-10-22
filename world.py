import numpy as np


class World:
    def __init__(self, time=0, rows=9, columns=10):
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def check_collision(self, position = [], plant = False):
        disallowed_directions = []

        if position[1] + 1 > self.rows:
            disallowed_directions.append(1)
        if position[1] - 1 < 1:
            disallowed_directions.append(2)
        if position[0] - 1 < 1:
            disallowed_directions.append(3)
        if position[1] + 1 > self.columns:
            disallowed_directions.append(4)

        if plant:
            for food in self.foodList:
                if position + np.array([0, 1]) == food:
                    disallowed_directions.append(1)
                if position + np.array([0, -1]) == food:
                    disallowed_directions.append(2)
                if position + np.array([-1, 0]) == food:
                    disallowed_directions.append(3)
                if position + np.array([1, 0]) == food:
                    disallowed_directions.append(4)

        list(set(disallowed_directions))
        return disallowed_directions

