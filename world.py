import random
from bug import Bug

class World:

    def __init__(self, time=0, rows=9, columns=10):
        self.time = time
        self.grid = [[None for i in range(rows)] for i in range(columns)]
        self.bugList = []
        self.foodList = []

    def add_bug(self):
        newBug = Bug()
