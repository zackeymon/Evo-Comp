import numpy as np
from direction import Direction as di

class Food:
       
    def __init__(self, position, energy, repThresh, energyMax): 
       self.position = np.array(position)
       self.energy = energy
       self.repThresh = repThresh
       self.energyMax = energyMax
       
    def get_energy_value(self):
        return self.energy
       
    def grow(self):
        self.energy += 1
              
    def reproduce(self, new, food_list):
        if self.energy >= self.repThresh:

                           
                     
            
    def die(self):
        if self.energy <= 0:
