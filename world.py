import random
import numpy as np
from bug import Bug
from food import Food
from organism_type import OrganismType
from direction import Direction


class World:
    """
    A class to create in the environment in which our organisms live.
    """

    def __init__(self, time=0, rows=10, columns=10, seed=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')):
        """
        World Initialisation
        :param time: Time at which the world begins to exist
        :param rows: Number of rows in the world
        :param columns: Number of columns in the world
        """
        self.seed = seed
        self.time = time
        self.columns = columns
        self.rows = rows
        self.grid = [[x, y] for x in range(columns) for y in range(rows)]
        self.bugList = []
        self.foodList = []
        self.bugListDead = []
        self.foodListDead = []
        self.food_data = {'time':[], 'population':[], ['dead_population'], ['average_alive_lifetime'],
                          ['average_lifespan']}
        self.bug_data = [['time'], ['population'], ['dead_population'], ['average_alive_lifetime'],
                         ['average_lifespan']]
        self.bug_gene_data = [[] for _ in range(2)]

    def random_position(self):
        x = random.randint(0, self.columns - 1)
        y = random.randint(0, self.rows - 1)
        return [x, y]

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
            for food in self.foodList:
                if (position == food.position).all():
                    return True
        elif organism_type == OrganismType.bug:
            for bug in self.bugList:
                if (position == bug.position).all():
                    return True

        return False

    def available_spaces(self):
        self.grid = [[x, y] for x in range(self.columns) for y in range(self.rows)]
        for food in self.foodList:
            self.grid.remove(food.position.tolist())
        for bug in self.bugList:
            self.grid.remove(bug.position.tolist())

    def spawn_food(self, number=10, energy=20, reproduction_threshold=30, energy_max=100):
        """Spawn food and check spawn square is available."""
        for i in range(number):
            try:
                self.foodList.append(
                    Food(self.grid.pop(random.randint(0, len(self.grid) - 1)), 0, energy, reproduction_threshold,
                         energy_max))
            except ValueError:
                break

    def spawn_bug(self, number=10, energy=5, reproduction_threshold=70, energy_max=100):
        """Spawn bugs and check spawn square is available, bugs only created upon initialisation."""
        for i in range(number):
            try:
                self.bugList.append(
                    Bug(self.grid.pop(random.randint(0, len(self.grid) - 1)), 0, energy, reproduction_threshold,
                        energy_max))
            except ValueError:
                break
