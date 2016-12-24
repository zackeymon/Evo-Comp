import numpy as np
import random


class Direction:
    """
    Define a direction for movement and reproduction.
    """
    up, down, left, right = range(4)

    @staticmethod
    def random(allowed_directions):
        """Pick a random direction from allowed directions."""

        if not allowed_directions:
            return None

        direction = random.choice(allowed_directions)
        return np.array(([0, 1], [0, -1], [-1, 0], [1, 0])[direction])
