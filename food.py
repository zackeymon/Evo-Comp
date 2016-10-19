import numpy as np

class Food:
       
    def __init__(self, position, energy):
        self.position = np.array(position)
        self.energy = energy
    
    def get_energy_value(self):
        return self.energy
    
    def grow(self):
        self.energy += 1
    
    def reproduce(self, new):
        if self.energy >= 20:
            spawnp = np.random.random_integers(4)
            
    def die(self):
        if self.energy <= 0:
