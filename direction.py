import numpy as np
from enum import Enum

class Direction(Enum):
  up = 1
  down = 2
  left = 3
  right = 4

  def random():
  random_point = np.random.random_integers(4)
  delx = 0
  dely = 0
    if random_point == Direction.up:
      dely += 1
    elif random_point == Direcion.down:
      dely -= 1
    elif random_point == Direction.left:
      delx -= 1
    elif random_point == Direction.right:
      delx += 1
      
