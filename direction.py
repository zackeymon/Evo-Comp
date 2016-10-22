import numpy as np
import random
from enum import Enum


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

    @staticmethod
    def random(disallowed_directions = []):
        directions = range(1, 4)
        allowed_directions = [x for x in directions if x not in disallowed_directions]
        random_direction = random.choice(allowed_directions)
        del_x = 0
        del_y = 0
        if random_direction == Direction.up:
            del_y += 1
        elif random_direction == Direction.down:
            del_y -= 1
        elif random_direction == Direction.left:
            del_x -= 1
        elif random_direction == Direction.right:
            del_x += 1
        return np.array([del_x, del_y])


