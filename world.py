import random
import datetime
import numpy as np
from bug import Bug
from food import Food
from organism_type import OrganismType
from direction import Direction


class World:
    """
    A class to create in the environment in which our organisms live.
    """

    def __init__(self, rows, columns, fertile_lands=None, seed=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')):
        """
        World Initialisation
        :param rows: Number of rows in the world
        :param columns: Number of columns in the world
        """
        self.time = 0
        self.columns = columns
        self.rows = rows
        self.seed = seed
        self.food_list = []
        self.bug_list = []
        self.dead_food_list = []
        self.dead_bug_list = []

        self.fertile_squares = []
        if fertile_lands is None:
            # Whole world is fertile
            self.fertile_squares = [[x, y] for x in range(self.columns) for y in range(self.rows)]
        else:
            for i in fertile_lands:
                min_x, min_y, max_x, max_y = i[0][0], i[0][1], i[1][0], i[1][1]
                self.fertile_squares += [[x, y] for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)]

        self.spawnable_squares = list(self.fertile_squares)

    def get_disallowed_directions(self, current_position, organism_type):
        """Each organism cannot collide with itself (no overlap)."""
        disallowed_directions = []

        if self.check_collision(current_position + np.array([0, 1]), organism_type):
            disallowed_directions.append(Direction.up)
        if self.check_collision(current_position + np.array([0, -1]), organism_type):
            disallowed_directions.append(Direction.down)
        if self.check_collision(current_position + np.array([-1, 0]), organism_type):
            disallowed_directions.append(Direction.left)
        if self.check_collision(current_position + np.array([1, 0]), organism_type):
            disallowed_directions.append(Direction.right)

        return disallowed_directions

    def check_collision(self, position, organism_type):
        """Check if position is out of bounds and for disallowed collisions."""
        if position[0] < 0 or position[0] >= self.columns or position[1] < 0 or position[1] >= self.rows:
            return True

        if organism_type == OrganismType.food:
            for food in self.food_list:
                if (position == food.position).all():
                    return True
        elif organism_type == OrganismType.bug:
            for bug in self.bug_list:
                if (position == bug.position).all():
                    return True

        return False

    def available_spaces(self):
        self.spawnable_squares = list(self.fertile_squares)
        for food in self.food_list:
            self.spawnable_squares.remove(food.position.tolist())

    def spawn_food(self, number, energy=20, reproduction_threshold=30, energy_max=100, gene_val=0.0):
        """Spawn food and check spawn square is available."""
        for i in range(number):
            try:
                self.food_list.append(
                    Food(self.spawnable_squares.pop(random.randint(0, len(self.spawnable_squares) - 1)), energy,
                         reproduction_threshold, energy_max, gene_val))
            except ValueError:
                break

    def spawn_bug(self, number, energy=15, reproduction_threshold=70, energy_max=100, gene_val=0.0):
        """Spawn bugs and check spawn square is available, bugs only created upon initialisation."""
        for i in range(number):
            try:
                self.bug_list.append(
                    Bug(self.spawnable_squares.pop(random.randint(0, len(self.spawnable_squares) - 1)), energy,
                        reproduction_threshold, energy_max, gene_val))
            except ValueError:
                break
