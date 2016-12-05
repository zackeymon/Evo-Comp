import numpy as np
import os
import csv
import colorsys
import evolution_switches as es
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
        self.world_data = OrderedDict([('organism', []), ('x', []), ('y', []), ('energy', []), ('taste', [])])

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

    @staticmethod
    def split_list(data):
        """Split the overall list of data into separate days."""
        split_data = [[]]
        for item in data:
            if "'end_day'" in item:
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
        
        data_to_generate = [{'list': self.world.food_list, 'name': 'food'},
                            {'list': self.world.bug_list, 'name': 'bug'}]
        
        for organism_type in data_to_generate:
            for organism in organism_type['list']:
                self.world_data['organism'].append(organism_type['name'])
                self.world_data['x'].append(organism.position[0])
                self.world_data['y'].append(organism.position[1])
                self.world_data['energy'].append(organism.energy)
                self.world_data['taste'].append(organism.taste)

        self.world_data['organism'].append('end_day')
        self.world_data['x'].append('end_day')
        self.world_data['y'].append('end_day')
        self.world_data['energy'].append('end_day')
        self.world_data['taste'].append('end_day')

    def output_view_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.world.seed, 'data_files', 'world_data.csv'), 'a') as world_file:
            for organism, x, y, energy, taste in zip(*self.world_data.values()):
                world_file.write('%r,' % organism + '%r,' % x + '%r,' % y + '%r,' % energy + '%r,' % taste + '\n')

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


    def view_world(self):
        """"Draw the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(self.world.columns, self.world.rows)).add_subplot(1, 1, 1)

        for food in self.world.food_list:
            if es.gene_value:
                color = colorsys.hsv_to_rgb(food.gene_val/360, 1, 1)
            else:
                color = 'g'

            food_size = food.energy*0.01
            if food_size <= 0.3:
                ax.add_patch(Rectangle((food.position[0]+(0.5-0.3/2), food.position[1]+(0.5-0.3/2)), 0.3, 0.3,
                                       facecolor=color))
            else:
                ax.add_patch(Rectangle((food.position[0]+(0.5-food_size/2), food.position[1]+(0.5-food_size/2)),
                                       food_size, food_size, facecolor=color))
                
        for bug in self.world.bug_list:
            bug_size = bug.energy*0.01
            if es.gene_value:
                color = 'r'
            else:
                color = colorsys.hsv_to_rgb(bug.gene_val/360, 1, 1)

            if bug_size <= 0.4:
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=0.4, height=0.4,
                                     facecolor='k'))
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=0.25, height=0.25,
                                     facecolor=color))
            else:
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size, height=bug_size,
                                     facecolor='k'))
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=bug_size/1.5,
                                     height=bug_size/1.5, facecolor=color))

        ax.set_xticks(np.arange(0, self.world.columns+1, 1))
        ax.set_yticks(np.arange(0, self.world.rows+1, 1))
        plt.title('time=%s' % self.world.time, fontsize=(2*self.world.columns))
#       ax.grid(b=True, which='major', color='black', linestyle='-')

        plt.savefig(os.path.join('data', self.world.seed, '%s.png' % self.world.time))
        plt.close()

    def generate_world_data(self):
        """Add data for the current world iteration to a list."""

        data_to_generate = [{'data': self.food_data, 'list': self.world.food_list, 'd_list': self.world.dead_food_list},
                            {'data': self.bug_data, 'list': self.world.bug_list, 'd_list': self.world.dead_bug_list}]

        for organism_type in data_to_generate:
            organism_type['data']['time'].append(self.world.time)
            organism_type['data']['energy'].append(self.sum_list_energy(organism_type['list']))
            organism_type['data']['population'].append(len(organism_type['list']))
            organism_type['data']['deaths'].append(sum([len(i) for i in organism_type['d_list'][-10:]]))
            organism_type['data']['average_alive_lifetime'].append(self.average_lifetime([organism_type['list']]))
            organism_type['data']['average_lifespan'].append(self.average_lifetime(organism_type['d_list'][-10:]))

    def output_world_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        data_to_output = [{'path': 'food_data', 'data': self.food_data.values()},
                          {'path': 'bug_data', 'data': self.bug_data.values()}]

        for organism_type in data_to_output:
            with open(os.path.join('data', self.world.seed, 'data_files',
                                   organism_type['path'] + '.csv'), 'a') as organism_file:
                for time, energy, population, dead_population, average_alive_lifetime, average_lifespan \
                        in zip(*organism_type['data']):
                    organism_file.write('%r,' % time + '%r,' % energy + '%r,' % population + '%r,' % dead_population
                                        + '%r,' % average_alive_lifetime + '%r,' % average_lifespan + '\n')

    def plot_world_data(self):
        """Read the CSV (comma-separated values) output and plot trends."""

        food_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'food_data.csv'), delimiter=',',
                                  names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                         'average_lifespan'])

        bug_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'bug_data.csv'), delimiter=',',
                                 names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                        'average_lifespan'])

        data_to_plot = []
        time = food_data['time']

        data1 = [(time, food_data['population'], 'Alive'), (time, food_data['dead_population'],
                                                            'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data1, 'x_label': 'Time', 'y_label': 'Number of Food', 'title': 'Food Populations',
                             'filename': 'food_population.png'})

        data2 = [(time, bug_data['population'], 'Alive'), (time, bug_data['dead_population'],
                                                           'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data2, 'x_label': 'Time', 'y_label': 'Number of Bugs', 'title': 'Bug Populations',
                             'filename': 'bug_population.png'})

        data3 = [(time, food_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (time, food_data['average_alive_lifetime'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data3, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Food Lifetimes',
                             'filename': 'food_lifetime.png'})

        data4 = [(time, bug_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (time, bug_data['average_lifespan'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data4, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Bug Lifetimes',
                             'filename': 'bug_lifetime.png'})

        data5 = [(time, food_data['population'], 'Food'), (time, bug_data['population'], 'Bugs'),
                 (time, food_data['population'] + bug_data['population'], 'Food + Bugs')]
        data_to_plot.append({'data': data5, 'x_label': 'Time', 'y_label': 'Number', 'title': 'World Population',
                             'filename': 'world_population.png'})

        data6 = [(time, food_data['energy'], 'Food'), (time, bug_data['energy'], 'Bugs'),
                 (time, food_data['energy'] + bug_data['energy'], 'Food + Bugs')]
        data_to_plot.append({'data': data6, 'x_label': 'Time', 'y_label': 'Energy', 'title': 'World Energy',
                             'filename': 'world_energy.png'})

        for data_dict in data_to_plot:
            plt.figure()
            for (x, y, l) in data_dict['data']:
                plt.plot(x, y, label=l)
            plt.xlabel(data_dict['x_label'])
            plt.ylabel(data_dict['y_label'])
            plt.legend()
            plt.title(data_dict['title'])
            plt.savefig(os.path.join('data', self.world.seed, data_dict['filename']))
            plt.close()
