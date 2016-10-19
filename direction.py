import numpy as np
from enum import Enum

class Direction(Enum):
  up = 1
  down = 2
  left = 3
  right = 4

  def random():
  randomP = np.random.random_integers(4)
  delx = 0
  dely = 0
    if randomP == Direction.up:
      dely += 1
    elif randomP == Direcion.down:
      dely -= 1
    elif randomP == Direction.left:
      delx -= 1
    elif randomP == Direction.right:
      delx += 1
      
