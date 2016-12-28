import os
from collections import OrderedDict
from shutil import move
from tempfile import mkstemp
from utility_methods import *


class WorldRecorder:
    """
    A class output the data for the world as it develops.
    """

    def __init__(self, world):
        """
        World Recorder Initialisation
        :param world: The world being recorded
        """
        self.world = world
        self.world_data = OrderedDict([('organism', []), ('x', []), ('y', []), ('energy', []),
                                       ('reproduction_threshold', []), ('taste', [])])

        # Initialise two dictionaries to store food and bug data
        food_dict, bug_dict = (OrderedDict
                               ([('time', []),
                                 ('energy', []),
                                 ('population', []),
                                 ('deaths', []),
                                 ('average_alive_lifetime', []),
                                 ('average_lifespan', [])])
                               for _ in range(2))

        self.organism_data = {'food': food_dict, 'bug': bug_dict}

        # Create output directories if they don't exist
        for path in ['world', 'data_files']:
            if not os.path.exists(os.path.join('data', world.seed, path)):
                os.makedirs(os.path.join('data', world.seed, path))

        # Create a copy of the config file with parameters of initialisation
        fd, new_path = mkstemp()
        with open(new_path, 'w') as new_file:
            with open('config.py') as old_file:
                for line in old_file:
                    new_file.write(line.replace('seed=None', 'seed=%r' % world.seed))
        os.close(fd)  # prevent file descriptor leakage
        move(new_path, os.path.join('data', world.seed, 'config.py'))  # move new file

    def generate_world_stats(self):
        """Add data for the current world iteration to a list."""

        for organism in ['food', 'bug']:
            alive = self.world.organism_lists[organism]['alive']
            dead = self.world.organism_lists[organism]['dead']

            self.organism_data[organism]['time'].append(self.world.time)
            self.organism_data[organism]['energy'].append(sum_list_energy(alive))
            self.organism_data[organism]['population'].append(len(alive))
            self.organism_data[organism]['deaths'].append(sum([len(i) for i in dead[-10:]]))
            self.organism_data[organism]['average_alive_lifetime'].append(average_lifetime([alive]))
            self.organism_data[organism]['average_lifespan'].append(average_lifetime(dead[-10:]))

    def output_world_stats(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        print('outputting world statistics...')

        for organism in ['food', 'bug']:
            with open(os.path.join('data', self.world.seed, 'data_files', str(organism) + '_data.csv'),
                      'w') as organism_file:
                for time, energy, population, dead_population, average_alive_lifetime, average_lifespan in zip(
                        *self.organism_data[organism].values()):
                    organism_file.write(
                        '%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population
                        + '%r,' % average_alive_lifetime + '%r,' % average_lifespan + '\n')

    def generate_world_data(self):
        """Add data for current world iteration to a list."""

        for organism in ['food', 'bug']:
            for individual_organism in self.world.organism_lists[organism]['alive']:
                self.world_data['organism'].append(organism)
                self.world_data['x'].append(individual_organism.position[0])
                self.world_data['y'].append(individual_organism.position[1])
                self.world_data['energy'].append(individual_organism.energy)
                self.world_data['reproduction_threshold'].append(individual_organism.reproduction_threshold)
                self.world_data['taste'].append(individual_organism.taste)

        # End day
        self.world_data['organism'].append(self.world.time)
        self.world_data['x'].append('end_day')
        self.world_data['y'].append('end_day')
        self.world_data['energy'].append('end_day')
        self.world_data['reproduction_threshold'].append('end_day')
        self.world_data['taste'].append('end_day')

    def output_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        print('outputting world data...')

        with open(os.path.join('data', self.world.seed, 'data_files', 'world_data.csv'), 'w') as world_file:
            for organism, x, y, energy, reproduction_threshold, taste in zip(*self.world_data.values()):
                world_file.write('%r,' % organism + '%r,' % x + '%r,' % y + '%r,' % energy
                                 + '%r,' % reproduction_threshold + '%r,' % taste + '\n')
