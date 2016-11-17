import unittest
from world import World


class WorldTests(unittest.TestCase):
    def test_one_by_one_world(self):
        my_world = World(rows=1, columns=1)
        my_world.available_spaces()
        self.assertEqual(my_world.grid, [[0, 0]])

        my_world.spawn_food(number=1)
        self.assertEqual(len(my_world.food_list), 1)
        self.assertEqual(my_world.grid, [])


if __name__ == '__main__':
    unittest.main()
