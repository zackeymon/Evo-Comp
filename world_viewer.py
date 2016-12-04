import numpy as np
import os
import csv
import colorsys
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse


class WorldViewer:
    """
    A class to view the world visually as it develops.
    """

    def __init__(self, world):
        """
        World Viewer Initialisation
        :param world: The world being viewed
        """
        self.world = world
        self.data = OrderedDict([('value', []), ('x', []), ('y', []), ('energy', []), ('taste', [])])

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
        if not os.path.exists(os.path.join('data', world.seed)):
            for i in ['world', 'data_files', 'food_gene_data', 'food_gene_space', 'bug_gene_data', 'bug_gene_space']:
                os.makedirs(os.path.join('data', world.seed, i))

        # Create the world_seeds file and write the headings if it doesn't exist
        if not os.path.isfile(os.path.join('data', 'world_seeds.csv')):
            with open(os.path.join('data', 'world_seeds.csv'), 'a') as seed:
                seed.write('time_stamp,' + 'columns,' + 'rows,' + 'food,' + 'bugs,' + 'results,' + '\n')

        with open(os.path.join('data', 'world_seeds.csv'), 'a') as seed:
            seed.write('%r,' % world.seed + '%r,' % world.columns + '%r,' % world.rows + '%r,'
                       % len(world.food_list) + '%r,' % len(world.bug_list) + '\n')

    @staticmethod
    def sum_list_lifetime(object_list, living=False):
        lifetime = 0

        if living is False:
            for i in object_list:
                for thing in i:
                    lifetime += thing.lifetime

            return lifetime

        else:
            for thing in object_list:
                lifetime += thing.lifetime

            return lifetime

    @staticmethod
    def sum_list_energy(object_list):
        energy = 0

        for thing in object_list:
            energy += thing.energy

        return energy

    @staticmethod
    def split_list(data):
        """Split the overall list of data into separate days."""
        split_data = [[]]
        for item in data:
            if "'none'" in item:
                split_data.append([])
            else:
                split_data[-1].append(item)

        data = split_data

        return data

    def view_world(self):
        """"Draw the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(self.world.columns, self.world.rows)).add_subplot(1, 1, 1)

        for food in self.world.food_list:  # draw a food
            food_size = food.energy * 0.01
            if food_size <= 0.3:
                ax.add_patch(
                    Rectangle((food.position[0] + (0.5 - 0.3 / 2), food.position[1] + (0.5 - 0.3 / 2)), 0.3, 0.3,
                              facecolor=colorsys.hsv_to_rgb(food.taste / 360, 1, 1)))
            else:
                ax.add_patch(
                    Rectangle((food.position[0] + (0.5 - food_size / 2), food.position[1] + (0.5 - food_size / 2)),
                              food_size, food_size, facecolor=colorsys.hsv_to_rgb(food.taste / 360, 1, 1)))

        for bug in self.world.bug_list:  # draw a bug (black edge)
            bug_size = bug.energy * 0.01
            if bug_size <= 0.4:
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=0.4, height=0.4,
                                     facecolor='k'))
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=0.25, height=0.25,
                                     facecolor=colorsys.hsv_to_rgb(bug.taste / 360, 1, 1)))
            else:
                ax.add_patch(
                    Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size, height=bug_size,
                            facecolor='k'))
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size / 1.5,
                                     height=bug_size / 1.5, facecolor=colorsys.hsv_to_rgb(bug.taste, 1, 1)))

        ax.set_xticks(np.arange(0, self.world.columns + 1, 1))
        ax.set_yticks(np.arange(0, self.world.rows + 1, 1))
        plt.title('time=%s' % self.world.time, fontsize=(2 * self.world.columns))

        plt.savefig(os.path.join('data', self.world.seed, 'world', '%s.png' % self.world.time))
        plt.close()

    def generate_view_world_data(self):
        """Add data for current world iteration to a list."""

        for food in self.world.food_list:
            self.data['value'].append('food')
            self.data['x'].append(food.position[0])
            self.data['y'].append(food.position[1])
            self.data['energy'].append(food.energy)
            self.data['taste'].append(food.taste)

        for bug in self.world.bug_list:
            self.data['value'].append('bug')
            self.data['x'].append(bug.position[0])
            self.data['y'].append(bug.position[1])
            self.data['energy'].append(bug.energy)
            self.data['taste'].append(bug.taste)

        self.data['value'].append('none')
        self.data['x'].append('none')
        self.data['y'].append('none')
        self.data['energy'].append('none')
        self.data['taste'].append('none')

    def output_view_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.world.seed, 'data_files', 'world_data.csv'), 'a') as world_file:
            for value, x, y, energy, taste in zip(*self.data.values()):
                world_file.write('%r,' % value + '%r,' % x + '%r,' % y + '%r,' % energy + '%r,' % taste + '\n')

    def plot_view_world_data(self):
        """Read the CSV (comma-separated values) output and plot the world."""
        csv_file = csv.reader(open(os.path.join('data', self.world.seed, 'data_files', 'world_data.csv')),
                              delimiter=",")
        organism_list = []
        for row in csv_file:
            row.remove(row[-1])  # remove the '\n' for CSV files
            organism_list.append(row)

        organism_list = self.split_list(organism_list)
        del organism_list[-1]

        for day in organism_list:
            for organism in day:
                for i in range(1, len(organism)):
                    organism[i] = float(organism[i])

        for i, day in enumerate(organism_list):

            ax = plt.figure(figsize=(self.world.columns, self.world.rows)).add_subplot(1, 1, 1)

            for organism in day:

                if organism[0] == "'food'":  # draw a food
                    food_size = organism[3] * 0.01
                    if food_size <= 0.3:
                        ax.add_patch(
                            Rectangle((organism[1] + (0.5 - 0.3 / 2), organism[2] + (0.5 - 0.3 / 2)), 0.3, 0.3,
                                      facecolor=colorsys.hsv_to_rgb(organism[4] / 360, 1, 1)))
                    else:
                        ax.add_patch(
                            Rectangle((organism[1] + (0.5 - food_size / 2), organism[2] + (0.5 - food_size / 2)),
                                      food_size, food_size, facecolor=colorsys.hsv_to_rgb(organism[4] / 360, 1, 1)))

                elif organism[0] == "'bug'":  # draw a bug(black edge)
                    bug_size = organism[3] * 0.01
                    if bug_size <= 0.4:
                        ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=0.4, height=0.4,
                                             facecolor='k'))
                        ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=0.25, height=0.25,
                                             facecolor=colorsys.hsv_to_rgb(organism[4] / 360, 1, 1)))
                    else:
                        ax.add_patch(
                            Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=bug_size, height=bug_size,
                                    facecolor='k'))
                        ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=bug_size / 1.5,
                                             height=bug_size / 1.5, facecolor=colorsys.hsv_to_rgb(organism[4], 1, 1)))

            ax.set_xticks(np.arange(0, self.world.columns + 1, 1))
            ax.set_yticks(np.arange(0, self.world.rows + 1, 1))
            plt.title('time=%s' % i, fontsize=(2 * self.world.columns))

            plt.savefig(os.path.join('data', self.world.seed, 'world', '%s.png' % i))
            plt.close()

    def generate_world_data(self):
        """Add data for the current world iteration to a list."""
        if self.world.time > 10:
            del self.world.dead_food_list[0]
            del self.world.dead_bug_list[0]

        self.food_data['time'].append(self.world.time)
        self.food_data['energy'].append(self.sum_list_energy(self.world.food_list))
        self.food_data['population'].append(len(self.world.food_list))
        self.food_data['deaths'].append(sum([len(i) for i in self.world.dead_food_list]))

        if len(self.world.food_list) == 0:
            self.food_data['average_alive_lifetime'].append(0)
        else:
            self.food_data['average_alive_lifetime'].append(
                self.sum_list_lifetime(self.world.food_list, living=True) / len(self.world.food_list))
        if sum([len(i) for i in self.world.dead_food_list]) == 0:
            self.food_data['average_lifespan'].append(0)
        else:
            self.food_data['average_lifespan'].append(
                self.sum_list_lifetime(self.world.dead_food_list) / sum([len(i) for i in self.world.dead_food_list]))

        self.bug_data['time'].append(self.world.time)
        self.bug_data['energy'].append(self.sum_list_energy(self.world.bug_list))
        self.bug_data['population'].append(len(self.world.bug_list))
        self.bug_data['deaths'].append(sum([len(i) for i in self.world.dead_bug_list]))
        if len(self.world.bug_list) == 0:
            self.bug_data['average_alive_lifetime'].append(0)
        else:
            self.bug_data['average_alive_lifetime'].append(
                self.sum_list_lifetime(self.world.bug_list, living=True) / len(self.world.bug_list))
        if sum([len(i) for i in self.world.dead_bug_list]) == 0:
            self.bug_data['average_lifespan'].append(0)
        else:
            self.bug_data['average_lifespan'].append(
                self.sum_list_lifetime(self.world.dead_bug_list) / sum([len(i) for i in self.world.dead_bug_list]))

    def output_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.world.seed, 'data_files', 'food_data.csv'), 'a') as food_file:
            for time, energy, population, dead_population, average_alive_lifetime, average_lifespan \
                    in zip(*self.food_data.values()):
                food_file.write('%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population + '%r,'
                                % average_alive_lifetime + '%r,' % average_lifespan + '\n')

        with open(os.path.join('data', self.world.seed, 'data_files', 'bug_data.csv'), 'a') as bug_file:
            for time, energy, population, dead_population, average_alive_lifetime, average_lifespan \
                    in zip(*self.bug_data.values()):
                bug_file.write('%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population + '%r,'
                               % average_alive_lifetime + '%r,' % average_lifespan + '\n')

    def plot_world_data(self):
        """Read the CSV (comma-separated values) output and plot trends."""

        food_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'food_data.csv'), delimiter=',',
                                  names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                         'average_lifespan'])

        plt.plot(food_data['time'], food_data['population'], label='Alive')
        plt.plot(food_data['time'], food_data['dead_population'], label='Deaths (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Number of Food')
        plt.legend()
        plt.title('Food Populations')
        plt.savefig(os.path.join('data', self.world.seed, 'food_population.png'))
        plt.close()

        plt.plot(food_data['time'], food_data['average_alive_lifetime'], label='Average Alive Lifetime')
        plt.plot(food_data['time'], food_data['average_lifespan'], label='Average Lifespan (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Lifetime')
        plt.legend()
        plt.title('Food Lifetimes')
        plt.savefig(os.path.join('data', self.world.seed, 'food_lifetime.png'))
        plt.close()

        bug_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'bug_data.csv'), delimiter=',',
                                 names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                        'average_lifespan'])

        plt.plot(bug_data['time'], bug_data['population'], label='Alive')
        plt.plot(bug_data['time'], bug_data['dead_population'], label='Deaths (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Number of Bugs')
        plt.legend()
        plt.title('Bug Populations')
        plt.savefig(os.path.join('data', self.world.seed, 'bug_population.png'))
        plt.close()

        plt.plot(bug_data['time'], bug_data['average_alive_lifetime'], label='Average Alive Lifetime')
        plt.plot(bug_data['time'], bug_data['average_lifespan'], label='Average Lifespan (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Lifetime')
        plt.legend()
        plt.title('Bug Lifetimes')
        plt.savefig(os.path.join('data', self.world.seed, 'bug_lifetime.png'))
        plt.close()

        plt.plot(food_data['time'], food_data['population'], label='Food')
        plt.plot(bug_data['time'], bug_data['population'], label='Bugs')
        plt.plot(food_data['time'], (food_data['population'] + bug_data['population']), label='Food + Bugs')
        plt.xlabel('Time')
        plt.ylabel('Number')
        plt.legend()
        plt.title('World Population')
        plt.savefig(os.path.join('data', self.world.seed, 'world_population.png'))
        plt.close()

        plt.plot(food_data['time'], food_data['energy'], label='Food')
        plt.plot(bug_data['time'], bug_data['energy'], label='Bugs')
        plt.plot(food_data['time'], (food_data['energy'] + bug_data['energy']), label='Food + Bugs')
        plt.xlabel('Time')
        plt.ylabel('Energy')
        plt.legend()
        plt.title('World Energy')
        plt.savefig(os.path.join('data', self.world.seed, 'world_energy.png'))
        plt.close()
