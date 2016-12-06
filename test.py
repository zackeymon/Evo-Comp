import unittest
from world import World
from world_viewer import WorldViewer
import numpy as np


class DummyBug():
    def __init__(self, lifetime=10):
        self.lifetime = lifetime


class WorldTests(unittest.TestCase):
    def test_grid_variable(self):
        my_world = World(rows=1, columns=1)
        my_world.available_spaces()
        self.assertEqual(my_world.spawnable_squares, [[0, 0]])

        my_world.spawn_food(number=1)
        self.assertEqual(len(my_world.food_list), 1)
        self.assertEqual(my_world.spawnable_squares, [])

    def test_fertile_lands(self):
        world2 = World(3, 3, fertile_lands=[[[1, 1], [1, 1]]])
        self.assertEqual(world2.fertile_squares, [[1, 1]])
        world2.spawn_food(1)
        world2.spawn_bug(1)
        self.assertEquals(len(world2.food_list), 1)
        self.assertEquals(len(world2.bug_list), 0)


class OrganismTests(unittest.TestCase):
    def setUp(self):
        self.my_world = World(rows=10, columns=10)
        self.tiny_world = World(rows=1, columns=1)

    def test_simple_spawn(self):
        self.my_world.spawn_bug(1, energy=30)
        self.my_world.spawn_food(2, reproduction_threshold=80)

        self.assertEqual(len(self.my_world.bug_list), 1)
        self.assertEqual(self.my_world.bug_list[0].energy, 30)
        self.assertEqual(len(self.my_world.food_list), 2)

        self.my_world.spawn_bug(2, energy_max=150)
        self.assertEqual(len(self.my_world.bug_list), 3)
        self.assertEqual(self.my_world.bug_list[1].energy_max, 150)

    def test_simple_reproduction(self):
        self.my_world.spawn_food(1, energy=61)
        old_food = self.my_world.food_list[0]
        new_food = old_food.reproduce([1, 0])

        self.assertEqual(old_food.energy, 30)
        self.assertEqual(new_food.energy, 30)


class WorldViewerTests(unittest.TestCase):
    def setUp(self):
        dummy_world = World(rows=10, columns=10, seed='lolz')
        self.dummy_bug_list = [DummyBug(10), DummyBug(20), DummyBug(30)]
        self.dead_dummy_bug_list = [[DummyBug(50), DummyBug(70), DummyBug(60)] for _ in range(20)]
        self.my_world_viewer = WorldViewer(dummy_world)

    def test_initialisation(self):
        self.my_world_viewer.food_data['time'].append(0)
        self.assertEqual(self.my_world_viewer.food_data['time'], [0])
        self.assertEqual(self.my_world_viewer.bug_data['time'], [])

    def test_average_lifetime_function(self):
        average_lifetime = self.my_world_viewer.average_lifetime([self.dummy_bug_list])
        self.assertEqual(average_lifetime, 20)

        average_dead_lifetime = self.my_world_viewer.average_lifetime(self.dead_dummy_bug_list[-10:])
        self.assertEqual(average_dead_lifetime, 60)


if __name__ == '__main__':
    unittest.main()
