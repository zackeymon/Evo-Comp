import os
from collections import OrderedDict
import evolution_switches as es


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

        # Initiate two dicts to store food and bug data
        self.food_data, self.bug_data = (OrderedDict
                                         ([('time', []),
                                           ('energy', []),
                                           ('population', []),
                                           ('deaths', []),
                                           ('average_alive_lifetime', []),
                                           ('average_lifespan', [])])
                                         for _ in range(2))

        # Create directories if they don't exist
        for path in ['world', 'data_files']:
            os.makedirs(os.path.join('data', world.seed, path))

        # Create seed file with parameters of initialisation
        with open(os.path.join('data', world.seed, 'data_files', world.seed + '.csv'), 'a') as seed:
            seed.write('columns,' + 'rows,' + 'food_rep_thresh_evo,' + 'bug_rep_thresh_evo,' + 'taste_evo,' + '\n')
            seed.write('%r,' % world.columns + '%r,' % world.rows + '%r,' % es.food_reproduction_threshold
                       + '%r,' % es.bug_reproduction_threshold + '%r,' % es.taste + '\n')

    @staticmethod
    def average_lifetime(organism_list):
        """organism_list[turn][organism_index]"""
        total_number = sum([len(i) for i in organism_list])
        if total_number == 0:
            return 0

        total_lifetime = sum([sum([i.lifetime for i in turn]) for turn in organism_list])

        return total_lifetime/total_number

    @staticmethod
    def sum_list_energy(object_list):
        energy = 0

        for thing in object_list:
            energy += thing.energy

        return energy

    def generate_world_stats(self):
        """Add data for the current world iteration to a list."""

        data_to_generate = [{'data': self.food_data, 'list': self.world.organism_lists['food']},
                            {'data': self.bug_data, 'list': self.world.organism_lists['bug']}]

        for organism_data in data_to_generate:
            organism_data['data']['time'].append(self.world.time)
            organism_data['data']['energy'].append(self.sum_list_energy(organism_data['list']['alive']))
            organism_data['data']['population'].append(len(organism_data['list']['alive']))
            organism_data['data']['deaths'].append(sum([len(i) for i in organism_data['list']['dead'][-10:]]))
            organism_data['data']['average_alive_lifetime'].append(
                self.average_lifetime([organism_data['list']['alive']]))
            organism_data['data']['average_lifespan'].append(self.average_lifetime(organism_data['list']['dead'][-10:]))

    def output_world_stats(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        print('outputting world statistics...')

        data_to_output = [{'data': self.food_data.values(), 'path': 'food_data'},
                          {'data': self.bug_data.values(), 'path': 'bug_data'}]

        for organism_data in data_to_output:
            with open(os.path.join('data', self.world.seed, 'data_files',
                                   organism_data['path'] + '.csv'), 'a') as organism_file:
                for time, energy, population, dead_population, average_alive_lifetime, average_lifespan \
                        in zip(*organism_data['data']):
                    organism_file.write('%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population
                                        + '%r,' % average_alive_lifetime + '%r,' % average_lifespan + '\n')

    def generate_world_data(self):
        """Add data for current world iteration to a list."""

        data_to_generate = [{'list': self.world.organism_lists['food']['alive'], 'name': 'food'},
                            {'list': self.world.organism_lists['bug']['alive'], 'name': 'bug'}]

        for organism_data in data_to_generate:
            for organism in organism_data['list']:
                self.world_data['organism'].append(organism_data['name'])
                self.world_data['x'].append(organism.position[0])
                self.world_data['y'].append(organism.position[1])
                self.world_data['energy'].append(organism.energy)
                self.world_data['reproduction_threshold'].append(organism.reproduction_threshold)
                self.world_data['taste'].append(organism.taste)

        self.world_data['organism'].append(self.world.time)
        self.world_data['x'].append('end_day')
        self.world_data['y'].append('end_day')
        self.world_data['energy'].append('end_day')
        self.world_data['reproduction_threshold'].append('end_day')
        self.world_data['taste'].append('end_day')

    def output_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        print('outputting world data...')

        with open(os.path.join('data', self.world.seed, 'data_files', 'world_data.csv'), 'a') as world_file:
            for organism, x, y, energy, reproduction_threshold, taste in zip(*self.world_data.values()):
                world_file.write('%r,' % organism + '%r,' % x + '%r,' % y + '%r,' % energy
                                 + '%r,' % reproduction_threshold + '%r,' % taste + '\n')
