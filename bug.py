import random

class Bug:

    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def eat(self, food):
        self.energy += food.energyVal

    def find_food(self, food_list):
        for food in food_list:
            if self.x == food.x and self.y == food.y:
                return food
        return None

    def move(self, bug_list, delx, dely):
        for bug in bug_list:
            if self.x + delx == bug.x and self.y + dely == bug.y:
                break

        self.x += delx
        self.y += dely

