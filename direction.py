import numpy as np
import random


class Direction:
    """
    Define a direction for movement and reproduction.
    """
    all_directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [0, -1], [1, -1]]

    @classmethod
    def random(cls, allowed_directions):
        """Pick a random direction from allowed directions."""

        if not allowed_directions:
            return None

        choice = random.choice(allowed_directions)
        return np.array(cls.all_directions[choice])
