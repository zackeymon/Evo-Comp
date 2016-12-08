import numpy as np
import os
import sys
import csv
import colorsys
import evolution_switches as es
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse


class WorldViewer:
    """
    A class to read data outputs and plot the results.
    """

    def __init__(self, seed):
        """
        Data Plotter Initialisation
        :param seed: The seed value for data to output
        """
        self.seed = seed

    @staticmethod
    def split_list(data):
        """Split the overall list of data into separate days."""
        split_data = [[]]
        for item in data:
            if "'end_day'" in item:
                split_data.append([])
            else:
                split_data[-1].append(item)

        del split_data[-1]
        data = split_data

        return data

    @staticmethod
    def view_world(world):
        """"Draw the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(world.columns, world.rows)).add_subplot(1, 1, 1)

        for food in world.organism_lists['food']['alive']:
            food_size = food.energy * 0.005

            if es.taste:
                hue = food.taste / 360
            else:
                hue = 0.33
            color = colorsys.hls_to_rgb(hue, 1.0 - food_size if food_size > 0.1 else 0.9, 1)

            ax.add_patch(Rectangle((food.position[0], food.position[1]), 1, 1, facecolor=color, linewidth=0))

        for bug in world.organism_lists['bug']['alive']:
            bug_size = bug.energy * 0.006
            if bug_size > 0.6:
                bug_size = 0.6

            if es.taste:
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=1, height=1,
                                     facecolor='k', linewidth=0))
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=0.7, height=0.7,
                                     facecolor=colorsys.hls_to_rgb(bug.taste / 360, bug_size + 0.2, 1), linewidth=0))

            else:
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=1, height=1,
                                     facecolor=colorsys.hls_to_rgb(0, bug_size + 0.2, 1), linewidth=0))

        ax.set_xticks(np.arange(0, world.columns + 1, 1))
        ax.set_yticks(np.arange(0, world.rows + 1, 1))
        plt.title('time=%s' % world.time, fontsize=(2 * world.columns))
        plt.savefig(os.path.join('data', world.seed, 'world', '%s.png' % world.time))
        plt.close()

    def plot_world_stats(self):
        """Read the CSV (comma-separated values) output and plot trends."""

        print('plotting world statistics...')

        data = [(np.genfromtxt(os.path.join('data', self.seed, 'data_files', path + '.csv'), delimiter=',',
                               names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                      'average_lifespan'])) for path in ['food_data', 'bug_data']]
        food_data, bug_data = data[0], data[1]

        data_to_plot = []
        time = food_data['time']

        data1 = [(food_data['population'], 'Alive'), (food_data['dead_population'], 'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data1, 'x_label': 'Time', 'y_label': 'Number of Food', 'title': 'Food Populations',
                             'filename': 'food_population.png'})

        data2 = [(bug_data['population'], 'Alive'), (bug_data['dead_population'], 'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data2, 'x_label': 'Time', 'y_label': 'Number of Bugs', 'title': 'Bug Populations',
                             'filename': 'bug_population.png'})

        data3 = [(food_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (food_data['average_alive_lifetime'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data3, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Food Lifetimes',
                             'filename': 'food_lifetime.png'})

        data4 = [(bug_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (bug_data['average_lifespan'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data4, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Bug Lifetimes',
                             'filename': 'bug_lifetime.png'})

        data5 = [(food_data['population'], 'Food'), (bug_data['population'], 'Bugs'),
                 (food_data['population'] + bug_data['population'], 'Food + Bugs')]
        data_to_plot.append({'data': data5, 'x_label': 'Time', 'y_label': 'Number', 'title': 'World Population',
                             'filename': 'world_population.png'})

        data6 = [(food_data['energy'], 'Food'), (bug_data['energy'], 'Bugs'),
                 (food_data['energy'] + bug_data['energy'], 'Food + Bugs')]
        data_to_plot.append({'data': data6, 'x_label': 'Time', 'y_label': 'Energy', 'title': 'World Energy',
                             'filename': 'world_energy.png'})

        for data_dict in data_to_plot:
            plt.figure()
            for (y, l) in data_dict['data']:
                plt.plot(time, y, label=l)
            plt.xlabel(data_dict['x_label'])
            plt.ylabel(data_dict['y_label'])
            plt.legend()
            plt.title(data_dict['title'])
            plt.savefig(os.path.join('data', self.seed, data_dict['filename']))
            plt.close()

    def plot_world_data(self, world=False):
        """Read the CSV (comma-separated values) output and plot the world and/or gene values for each time."""

        settings_file = csv.DictReader(open(os.path.join('data', self.seed, 'data_files', self.seed + '.csv')))
        for row in settings_file:
            row.pop('', None)
            row['columns'], row['rows'] = float(row['columns']), float(row['rows'])
            settings = row

        if settings['food_rep_thresh_evo'] or settings['bug_rep_thresh_evo'] == 'True':
            for path in ['food_gene_data', 'bug_gene_data']:
                if not os.path.exists(os.path.join('data', self.seed, path)):
                    os.makedirs(os.path.join('data', self.seed, path))
        if settings['taste_evo'] == 'True':
            for path in ['food_gene_space', 'bug_gene_space']:
                if not os.path.exists(os.path.join('data', self.seed, path)):
                    os.makedirs(os.path.join('data', self.seed, path))

        world_file = csv.reader(open(os.path.join('data', self.seed, 'data_files', 'world_data.csv')), delimiter=',')

        organism_list = []
        for row in world_file:
            row.remove(row[-1])  # remove the '\n' for CSV files
            organism_list.append(row)

        organism_list = [[[float(organism[i]) if i > 0 else organism[i] for i in range(len(organism))]
                          for organism in day] for day in self.split_list(organism_list)]

        for i, day in enumerate(organism_list):

            sys.stdout.write('\r' + 'plotting world data, time: %r' % i + '/%r' % (len(organism_list) - 1) + '...')
            sys.stdout.flush()

            if world:

                ax = plt.figure(figsize=(settings['columns'], settings['rows'])).add_subplot(1, 1, 1)

                for organism in day:

                    if organism[0] == "'food'":  # draw a food
                        food_size = organism[3] * 0.005

                        if settings['taste_evo'] == 'True':
                            hue = organism[5] / 360
                        else:
                            hue = 0.33
                        color = colorsys.hls_to_rgb(hue, 1.0 - food_size if food_size > 0.1 else 0.9, 1)

                        ax.add_patch(
                            Rectangle((organism[1], organism[2]), 1, 1, facecolor=color, linewidth=0))

                    elif organism[0] == "'bug'":  # draw a bug
                        bug_size = organism[3] * 0.006
                        if bug_size > 0.6:
                            bug_size = 0.6

                        if settings['taste_evo'] == 'True':  # black outline
                            ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=1, height=1,
                                                 facecolor='k', linewidth=0))
                            ax.add_patch(
                                Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=0.7, height=0.7,
                                        facecolor=colorsys.hls_to_rgb(0, bug_size + 0.2, 1), linewidth=0))

                        else:  # no outline
                            ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=1, height=1,
                                                 facecolor=colorsys.hls_to_rgb(organism[5] / 360, bug_size + 0.2, 1),
                                                 linewidth=0))

                ax.set_xticks(np.arange(0, settings['columns'] + 1, 1))
                ax.set_yticks(np.arange(0, settings['rows'] + 1, 1))
                plt.title('time=%s' % i, fontsize=(2 * settings['columns']))
                plt.savefig(os.path.join('data', self.seed, 'world', '%s.png' % i))
                plt.close()

            if settings['food_rep_thresh_evo'] or settings['bug_rep_thresh_evo'] or settings['taste_evo'] == 'True':

                food_list = []
                bug_list = []

                for organism in day:
                    if organism[0] == "'food'":
                        food_list.append(organism)
                    elif organism[0] == "'bug'":
                        bug_list.append(organism)

                data_to_plot = [{'data': food_list, 'path': 'food_gene_data', 'colour': 'g',
                                 'colour_maps': 'Greens', 'path2': 'food_gene_space'},
                                {'data': bug_list, 'path': 'bug_gene_data', 'colour': 'r',
                                 'colour_maps': 'Reds', 'path2': 'bug_gene_space'}]

                for organism_data in data_to_plot:

                    # 1D Plot (bar chart)
                    if settings['food_rep_thresh_evo'] or settings['bug_rep_thresh_evo'] == 'True':

                        rep_dict = {j: 0 for j in range(101)}

                        for organism in organism_data['data']:
                            # count number of occurrences of each reproduction threshold for each time
                            rep_dict[organism[4]] += 1

                        y_pos = np.arange(len(rep_dict.keys()))
                        total = sum(rep_dict.values())
                        if total > 0:
                            for key, value in rep_dict.items():
                                rep_dict[key] = value / total  # normalisation

                        plt.bar(y_pos, rep_dict.values(), align='center', color=organism_data['colour'])
                        plt.xlabel('Reproduction Threshold')
                        plt.ylabel('Population')
                        plt.title('time=%s' % i)
                        plt.savefig(os.path.join('data', self.seed, organism_data['path'], '%s.png' % i))
                        plt.close()

                    # 2D Plot (heat map)
                    if settings['taste_evo'] == 'True':

                        rep_thresh = []
                        taste = []

                        for organism in organism_data['data']:
                            rep_thresh.append(organism[4])
                            taste.append(organism[5])

                        x = [i for i in range(51)]
                        y = [i for i in range(61)]

                        rep_thresh = [int(j / 2) for j in rep_thresh]  # bin values
                        taste = [int(j / 6) for j in taste]

                        z = [[0 for _ in range(len(x))] for _ in range(len(y))]
                        z_list = [list(i) for i in zip(rep_thresh, taste)]

                        for coordinates in z_list:
                            z[coordinates[1]][coordinates[0]] += 1 / len(z_list)  # list of population frequencies

                        x = [j * 2 for j in x]
                        y = [j * 6 for j in y]

                        xi, yi = np.meshgrid(x, y)
                        zi = np.array(z)

                        plt.pcolormesh(xi, yi, zi, cmap=organism_data['colour_maps'])
                        plt.colorbar()
                        plt.xlim(0, 101)
                        plt.ylim(0, 359)
                        plt.xlabel('Reproduction Threshold')
                        plt.ylabel('Taste')
                        plt.title('time=%s' % i)
                        plt.savefig(os.path.join('data', self.seed, organism_data['path2'], '%s.png' % i))
                        plt.close()
