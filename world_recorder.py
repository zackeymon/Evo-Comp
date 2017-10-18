import os
from collections import OrderedDict
from shutil import move
from tempfile import mkstemp
from utility_methods import *


class WorldRecorder:
    """
    A class to output the data for the world as it develops.
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
                                 ('average_deaths', []),
                                 ('average_alive_lifetime', []),
                                 ('average_lifespan', []),
                                 ('average_reproduction_threshold', [])])
                               for _ in range(2))

        self.organism_data = {'food': food_dict, 'bug': bug_dict}

        # Create output directories if they don't exist
        for path in ['world', 'data_files']:
            if not os.path.exists(os.path.join('data', world.seed, path)):
                os.makedirs(os.path.join('data', world.seed, path))

        if not os.path.exists(os.path.join('data', world.seed, 'data_files', 'world_data')):
            os.makedirs(os.path.join('data', world.seed, 'data_files', 'world_data'))

        # Create a copy of the config file with parameters of initialisation
        fd, new_path = mkstemp()
        with open(new_path, 'w') as new_file:
            with open('config.py') as old_file:
                for line in old_file:
                    new_file.write(line.replace('seed=None', 'seed=%r' % world.seed))
        os.close(fd)  # prevent file descriptor leakage
        move(new_path, os.path.join('data', world.seed, 'config.py'))  # move new file

    def generate_world_stats(self):
        """Add statistics for the current world iteration to a list."""

        world_param = ['time', 'energy', 'population', 'deaths', 'average_deaths', 'average_alive_lifetime',
                       'average_lifespan', 'average_reproduction_threshold']

        for organism in ['food', 'bug']:
            alive = self.world.organism_lists[organism]['alive']
            dead = self.world.organism_lists[organism]['dead']

            world_append = [self.world.time, sum_list_energy(alive), len(alive), len(dead[-1]),
                            sum([len(i) for i in dead[-10:]]) / 10, average_lifetime([alive]),
                            average_lifetime(dead[-10:]), average_rep_thresh([alive])]

            for param_list, x in zip(world_param, world_append):
                self.organism_data[organism][param_list].append(x)

    def output_world_stats(self):
        """Output statistics in CSV (comma-separated values) format for analysis."""

        print('outputting world statistics...')

        for organism in ['food', 'bug']:
            with open(os.path.join('data', self.world.seed, 'data_files', str(organism) + '_data.csv'),
                      'w') as organism_file:
                for time, energy, population, dead_population, average_dead_population, average_alive_lifetime, \
                        average_lifespan, average_reproduction_threshold in zip(*self.organism_data[organism].values()):
                    organism_file.write(
                        '%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population
                        + '%r,' % average_dead_population + '%r,' % average_alive_lifetime + '%r,' % average_lifespan
                        + '%r,' % average_reproduction_threshold + '\n')

    def generate_world_data(self):
        """Add data for the current world iteration to a list."""

        organism_param = ['organism', 'x', 'y', 'energy', 'reproduction_threshold', 'taste']

        # Start day
        for param_list in organism_param:
            del self.world_data[param_list][:]

        for organism in ['food', 'bug']:
            for individual_organism in self.world.organism_lists[organism]['alive']:
                organism_append = [organism, individual_organism.position[0], individual_organism.position[1],
                                   individual_organism.energy, individual_organism.reproduction_threshold,
                                   individual_organism.taste]

                for param_list, x in zip(organism_param, organism_append):
                    self.world_data[param_list].append(x)

    def output_world_data(self):
        """Output data in CSV (comma-separated values) format for each day."""

        organism_param = ['organism', 'x', 'y', 'energy', 'reproduction_threshold', 'taste']

        with open(os.path.join('data', self.world.seed, 'data_files', 'world_data',
                               '%r.csv' % self.world.time), 'w') as world_file:
            for organism, x, y, energy, reproduction_threshold, taste in zip(
                    *[self.world_data[param_list] for param_list in organism_param]):
                world_file.write('%r,' % organism + '%r,' % x + '%r,' % y + '%r,' % energy
                                 + '%r,' % reproduction_threshold + '%r,' % taste + '\n')
