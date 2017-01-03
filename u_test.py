import unittest
import config as cfg
from utility_methods import *
from constants import *
from world import World
from world_recorder import WorldRecorder


class DummyBug:
    def __init__(self, energy=5, lifetime=10):
        self.energy = energy
        self.lifetime = lifetime


class WorldTests(unittest.TestCase):
    def test_grid_variable(self):
        world0 = World(rows=1, columns=1)
        world0.update_available_spawn_squares()
        self.assertEqual(world0.spawnable_squares, [[0, 0]])

        world0.drop_food(1)
        self.assertEqual(len(world0.organism_lists[FOOD_NAME]['alive']), 1)
        self.assertEqual(world0.spawnable_squares, [])

    def test_fertile_lands(self):
        world2 = World(rows=3, columns=3, fertile_lands=[[[1, 1], [1, 1]]])
        self.assertEqual(world2.fertile_squares, [[1, 1]])
        world2.drop_food(1)
        world2.drop_bug(1)
        self.assertEqual(len(world2.organism_lists[FOOD_NAME]['alive']), 1)
        self.assertEqual(len(world2.organism_lists[BUG_NAME]['alive']), 0)


class OrganismTests(unittest.TestCase):
    def setUp(self):
        self.my_world = World(rows=10, columns=10)
        self.tiny_world = World(rows=1, columns=1)

    def test_simple_spawn(self):
        self.my_world.drop_bug(1, energy=30)
        self.my_world.drop_food(2, reproduction_threshold=80)

        self.assertEqual(len(self.my_world.organism_lists[BUG_NAME]['alive']), 1)
        self.assertEqual(self.my_world.organism_lists[BUG_NAME]['alive'][0].energy, 30)
        self.assertEqual(len(self.my_world.organism_lists[FOOD_NAME]['alive']), 2)

        self.my_world.drop_bug(2, energy_max=150)
        self.assertEqual(len(self.my_world.organism_lists[BUG_NAME]['alive']), 3)
        self.assertEqual(self.my_world.organism_lists[BUG_NAME]['alive'][1].energy_max, 150)

    def test_simple_reproduction(self):
        self.my_world.drop_food(1, energy=61)
        old_food = self.my_world.organism_lists[FOOD_NAME]['alive'][0]
        new_food = old_food.reproduce([1, 0])

        self.assertEqual(old_food.energy, 30)
        self.assertEqual(new_food.energy, 30)

    def test_kill(self):
        self.my_world.drop_bug(3)
        self.my_world.organism_lists[BUG_NAME]['dead'].append([])
        self.my_world.kill(self.my_world.organism_lists[BUG_NAME]['alive'][0])
        self.assertEqual(len(self.my_world.organism_lists[BUG_NAME]['alive']), 2)
        self.assertEqual(len(self.my_world.organism_lists[BUG_NAME]['dead']), 1)

    def test_kwargs_override(self):
        self.tiny_world.drop_bug(1, **cfg.world['bug_spawn_vals'])
        self.assertEqual(self.tiny_world.organism_lists[BUG_NAME]['alive'][0].energy_max,
                         cfg.world['bug_spawn_vals']['energy_max'])


class WorldRecorderTests(unittest.TestCase):
    def setUp(self):
        dummy_world = World(rows=10, columns=10, seed='lolz')
        self.dummy_bug_list = [DummyBug(5, 10), DummyBug(10, 20), DummyBug(15, 30)]
        self.dead_dummy_bug_list = [[DummyBug(40, 50), DummyBug(60, 70), DummyBug(50, 60)] for _ in range(20)]
        self.my_world_recorder = WorldRecorder(dummy_world)

    def test_initialisation(self):
        self.my_world_recorder.organism_data['food']['time'].append(0)
        self.assertEqual(self.my_world_recorder.organism_data['food']['time'], [0])
        self.assertEqual(self.my_world_recorder.organism_data['bug']['time'], [])

    def test_sum_list_energy(self):
        total_alive_energy = sum_list_energy(self.dummy_bug_list)
        self.assertEqual(total_alive_energy, 30)

        total_dead_energy = sum_list_energy(self.dead_dummy_bug_list[0])
        self.assertEqual(total_dead_energy, 150)

    def test_average_lifetime_function(self):
        average_alive_lifetime = average_lifetime([self.dummy_bug_list])
        self.assertEqual(average_alive_lifetime, 20)

        average_dead_lifetime = average_lifetime(self.dead_dummy_bug_list[-10:])
        self.assertEqual(average_dead_lifetime, 60)


if __name__ == '__main__':
    unittest.main()
