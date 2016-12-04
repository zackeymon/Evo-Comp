import unittest
from world import World


class WorldTests(unittest.TestCase):
    def test_grid_variable(self):
        my_world = World(rows=1, columns=1)
        my_world.available_spaces()
        self.assertEqual(my_world.grid, [[0, 0]])

        my_world.spawn_food(number=1)
        self.assertEqual(len(my_world.food_list), 1)
        self.assertEqual(my_world.grid, [])


class OrganismTests(unittest.TestCase):
    def setUp(self):
        self.my_world = World(rows=10, columns=10)

    def test_simple_spawn(self):
        self.my_world.spawn_bug(1, energy=30)
        self.my_world.spawn_food(2, reproduction_threshold=80)

        self.assertEqual(len(self.my_world.bug_list), 1)
        self.assertEqual(self.my_world.bug_list[0].energy, 30)
        self.assertEqual(len(self.my_world.food_list), 2)
        self.assertEqual(self.my_world.food_list[0].reproduction_threshold, 80)

        self.my_world.spawn_bug(2, energy_max=150)
        self.assertEqual(len(self.my_world.bug_list), 3)
        self.assertEqual(self.my_world.bug_list[1].energy_max, 150)

        self.my_world.spawn_food(1, taste=1.0)
        self.assertEqual(len(self.my_world.food_list), 3)
        self.assertEqual(self.my_world.food_list[2].taste, 1.0)

    def test_simple_reproduction(self):
        self.my_world.spawn_food(1, energy=61)
        old_food = self.my_world.food_list[0]
        new_food = old_food.reproduce([1, 0])

        self.assertEqual(old_food.energy, 30)
        self.assertEqual(new_food.energy, 30)


if __name__ == '__main__':
    unittest.main()
