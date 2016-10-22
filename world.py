import numpy as np


class World:
    def __init__(self, time=0, rows=9, columns=10):
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def check_collision_food(self, food_position = []):
        food_disallowed_directions = []

        if food_position[1] + 1 > self.rows:
            food_disallowed_directions.append(1)
        elif food_position[1] - 1 < 1:
            food_disallowed_directions.append(2)
        elif food_position[0] - 1 < 1:
            food_disallowed_directions.append(3)
        elif food_position[1] + 1 > self.columns:
            food_disallowed_directions.append(4)

        for food in self.foodList:
            if food_position + [0, 1] == food:
                food_disallowed_directions.append(1)
            elif food_position + [0, -1] == food:
                food_disallowed_directions.append(2)
            elif food_position + [-1, 0] == food:
                food_disallowed_directions.append(3)
            elif food_position + [1, 0] == food:
                food_disallowed_directions.append(4)

        list(set(food_disallowed_directions))
        return np.array(food_disallowed_directions)

    def check_collision_bug(self, bug_position = []):
        bug_disallowed_directions = []

        if bug_position[1] + 1 > self.rows:
            bug_disallowed_directions.append(1)
        elif bug_position[1] - 1 < 1:
            bug_disallowed_directions.append(2)
        elif bug_position[0] - 1 < 1:
            bug_disallowed_directions.append(3)
        elif bug_position[1] + 1 > self.columns:
            bug_disallowed_directions.append(4)

        list(set(bug_disallowed_directions))
        return np.array(bug_disallowed_directions)

