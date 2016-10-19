import numpy as np
from direction import Direction 

class Food:
       
    def __init__(self, position, energy, reproduction_threshold, energy_max): 
       self.__position = np.array(position)
       self.__energy = energy
       self.__energy_intial = energy
       self.__reproduction_threshold = reproduction_threshold
       self.__energy_max = energy_max
       
    def get_energy_value(self):
        return self.energy
       
    def grow(self):
       if self.__energy < self.__energy_max:
              self.energy += 1
              
    def reproduce(self, new_food):
       #check for overlap
       del_position = Direction.random()
       new_position = self.__position + del_position
       new_energy = self.__energy_initial
       new_reproduction_threshold = self.__reproduction_threshold
       new_energy_max = self.__energy_max
       
       new_food = Food(new_position, new_energy, new_reproduction_threshold, new_energy_max)
       return new_food
 
