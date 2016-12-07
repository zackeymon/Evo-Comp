import numpy as np
import datetime
import random
from direction import Direction
from bug import Bug
from food import Food
from organism_type import OrganismType


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
        self.food_taste_average = 0.0
        self.food_taste_average = 0.0
        random.seed(self.seed)

        # Initiate two dicts to store lists of food and bugs
        food_lists, bug_lists = ({'alive': [], 'dead': []} for _ in range(2))
        self.organism_lists = {'food': food_lists, 'bug': bug_lists}

        self.grid = np.zeros(shape=(rows, columns))
        self.fertile_squares = []
        if fertile_lands is None:
            # Make the whole world fertile
            self.fertile_squares = [[x, y] for x in range(self.columns) for y in range(self.rows)]
        else:
            for i in fertile_lands:
                min_x, min_y, max_x, max_y = i[0][0], i[0][1], i[1][0], i[1][1]
                self.fertile_squares += [[x, y] for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]

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
        # Collide with wall
        if position[0] < 0 or position[0] >= self.columns or position[1] < 0 or position[1] >= self.rows:
            return True

        # Collide with organism of the same type
        if self.grid[tuple(position)] == organism_type or self.grid[tuple(position)] == OrganismType.food_bug:
            return True

        return False

    def available_spaces(self):
        """Get available spawn spaces and the average of the food taste value."""
        self.spawnable_squares = list(self.fertile_squares)
        food_taste_list = []

        for food in self.organism_lists['food']['alive']:

            try:
                self.spawnable_squares.remove(food.position.tolist())
            except ValueError:
                pass

            if food.taste >= 180:
                food_taste_list.append(food.taste - 360)
            else:
                food_taste_list.append(food.taste)

            self.food_taste_average = np.average(food_taste_list)
            # NaN != NaN
            if self.food_taste_average != self.food_taste_average:
                self.food_taste_average = 0.0

    def kill(self, organism):
        death_position = organism.position

        if organism.__class__ == Food:
            self.organism_lists['food']['dead'][-1].append(organism)
            self.organism_lists['food']['alive'].remove(organism)
            self.grid[tuple(death_position)] -= OrganismType.food

        elif organism.__class__ == Bug:
            self.organism_lists['bug']['dead'][-1].append(organism)
            self.organism_lists['bug']['alive'].remove(organism)
            self.grid[tuple(death_position)] -= OrganismType.bug

    def spawn_food(self, number, energy=20, reproduction_threshold=30, energy_max=100, taste=0.0):
        """Spawn food and check spawn square is available."""
        for i in range(number):
            try:
                spawn_position = self.spawnable_squares.pop(random.randint(0, len(self.spawnable_squares) - 1))
                self.organism_lists['food']['alive'].append(
                    Food(spawn_position, energy, reproduction_threshold, energy_max, taste))
                self.grid[tuple(spawn_position)] += OrganismType.food
            except ValueError:
                break

    def spawn_bug(self, number, energy=15, reproduction_threshold=70, energy_max=100, taste=0.0, random_spawn=False):
        """Spawn bugs and check spawn square is available, bugs only created upon initialisation."""
        spawn_squares = self.spawnable_squares
        if random_spawn:
            spawn_squares = [[x, y] for x in range(self.columns) for y in range(self.rows)]

        for i in range(number):
            try:
                spawn_position = self.spawnable_squares.pop(random.randint(0, len(spawn_squares) - 1))
                self.organism_lists['bug']['alive'].append(
                    Bug(spawn_position, energy, reproduction_threshold, energy_max, taste))
                self.grid[tuple(spawn_position)] += OrganismType.bug
            except ValueError:
                break
