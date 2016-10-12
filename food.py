class Food:

    def __init__(self, x, y, energyVal):
        self.x = x
        self.y = y
        self.energyVal = energyVal

    def get_energy_value(self):
        return self.energyVal