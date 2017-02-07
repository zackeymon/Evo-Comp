import numpy as np
import datetime
import random
import config as cfg
from constants import *
from utility_methods import get_taste_average
from bug import Bug
from food import Food


class World:
    """
    A class to create the environment inhabited by organisms.
    """

    def __init__(self, rows, columns, seed=None, fertile_lands=None, time=0, init_food=0, init_bugs=0):
        """
        World Initialisation
        :param rows: The number of rows in the world
        :param columns: The number of columns in the world
        :param seed: The random seed of the world
        :param fertile_lands: The areas on which organisms can spawn, random spawn by default
        :param time: The time the world has existed for
        :param init_food: The initial number of food in the world
        :param init_bugs: The initial number of bugs in the world
        """
        self.columns = columns
        self.rows = rows
        self.time = time
        self.seed = seed if seed is not None else datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        random.seed(self.seed)

        # Initiate a dict to store lists of food and bugs
        self.organism_lists = {FOOD_NAME: {'alive': [], 'dead': [[]]}, BUG_NAME: {'alive': [], 'dead': [[]]}}
        self.plant_position_dict = None
        self.grid = np.zeros(shape=(rows, columns), dtype=np.int)
        self.fertile_squares = self.get_fertile_squares(fertile_lands)
        self.spawnable_squares = list(self.fertile_squares)

        self.plant_position_dict = {}

        # Populate the world
        self.drop_food(init_food, **cfg.world['food_spawn_vals'])
        self.drop_bug(init_bugs, **cfg.world['bug_spawn_vals'])

    def prepare_today(self):
        """Returns lists of alive plant and bug objects."""

        alive_plants = self.organism_lists[FOOD_NAME]['alive']
        alive_bugs = self.organism_lists[BUG_NAME]['alive']

        # Display yesterday's data
        print("time: {}, plants: {}, bugs: {}".format(self.time, len(alive_plants), len(alive_bugs)))

        # It's a new day!
        self.time += 1
        self.update_available_spawn_squares()

        # if self.time == 200:
        #     self.spawn(Bug([int(self.rows/2), int(self.columns/2)], taste=180, **cfg.world['bug_spawn_vals']))

        # If there is still food, find their taste average, else don't update my average

        food_taste_average = get_taste_average([i.taste for i in alive_plants]) if alive_plants else \
            cfg.world['food_spawn_vals']['taste']
        bug_taste_average = get_taste_average([i.taste for i in alive_bugs]) if alive_bugs else \
            cfg.world['bug_spawn_vals']['taste']

        food_spawn_vals, bug_spawn_vals = [dict((k, v) for k, v in cfg.world[organism].items() if k is not 'taste') for
                                           organism in ['food_spawn_vals', 'bug_spawn_vals']]

        if self.time < cfg.endangered_time:
            # Drop balls on them (if endangered)
            if len(alive_plants) < cfg.food_endangered_threshold:
                self.drop_food(1, **food_spawn_vals, taste=food_taste_average)
            if len(alive_bugs) < cfg.bug_endangered_threshold:
                self.drop_bug(1, **bug_spawn_vals, taste=bug_taste_average)

        # Shuffle the order alive food & bug lists
        random.shuffle(alive_plants)
        random.shuffle(alive_bugs)

        # Initialise today's dead list
        self.organism_lists[FOOD_NAME]['dead'].append([])
        self.organism_lists[BUG_NAME]['dead'].append([])

        # Only keep death records for 10 days
        if len(self.organism_lists[FOOD_NAME]['dead']) > 10:
            del self.organism_lists[FOOD_NAME]['dead'][0]
            del self.organism_lists[BUG_NAME]['dead'][0]

        return alive_plants, alive_bugs

    def get_fertile_squares(self, fertile_lands):

        if fertile_lands is None:
            # Make the whole world fertile
            squares = [[x, y] for x in range(self.columns) for y in range(self.rows)]
        else:
            squares = []
            for i in fertile_lands:
                min_x, min_y, max_x, max_y = i[0][0], i[0][1], i[1][0], i[1][1]
                squares += [[x, y] for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]

        return squares

    def available(self, organism, direction):
        return not self._collide(organism.position + direction, organism.value)

    def _collide(self, position, organism_value):
        """Check if position is out of bounds and for disallowed collisions."""

        # Collide with wall
        if position[0] < 0 or position[0] >= self.columns or position[1] < 0 or position[1] >= self.rows:
            return True

        # Collide with organism of the same type
        if self.grid[tuple(position)] == organism_value or self.grid[tuple(position)] == FOOD_VAL + BUG_VAL:
            return True

        return False

    def update_available_spawn_squares(self):
        """Get available spawn spaces and the average of the food taste value for."""
        self.spawnable_squares = list(self.fertile_squares)

        i = 0
        while i < len(self.spawnable_squares):
            current_square = tuple(self.spawnable_squares[i])
            if self.grid[current_square] != EMPTY_SQUARE_VAL:
                del self.spawnable_squares[i]
                continue
            i += 1

    def kill(self, organism):
        self.grid[tuple(organism.position)] -= organism.value
        self.organism_lists[organism.name]['dead'][-1].append(organism)
        self.organism_lists[organism.name]['alive'].remove(organism)
        if organism.name == FOOD_NAME:
            del self.plant_position_dict[tuple(organism.position)]

    def spawn(self, organism):
        self.grid[tuple(organism.position)] += organism.value
        self.organism_lists[organism.name]['alive'].append(organism)
        if organism.name == FOOD_NAME:
            self.plant_position_dict[tuple(organism.position)] = organism

    def drop_food(self, number, energy=20, reproduction_threshold=30, energy_max=100, taste=180):
        """Spawn food on fertile land and check spawn square is available."""
        for _ in range(number):
            try:
                spawn_position = self.spawnable_squares.pop(random.randint(0, len(self.spawnable_squares) - 1))
                self.spawn(Food(spawn_position, energy, reproduction_threshold, energy_max, taste))
            except ValueError:
                break

    def drop_bug(self, number, energy=30, reproduction_threshold=70, energy_max=100, taste=180):
        """Spawn bugs on fertile land and check spawn square is available."""
        for _ in range(number):
            try:
                spawn_position = self.spawnable_squares.pop(random.randint(0, len(self.spawnable_squares) - 1))
                self.spawn(Bug(spawn_position, energy, reproduction_threshold, energy_max, taste))
            except ValueError:
                break
