import os
import sys
import csv
import colorsys
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse
from utility_methods import *
import evolution_switches as es


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
    def view_world(world):
        """"Plot the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)

        for food in world.organism_lists['food']['alive']:  # draw food
            hue = float(food.taste) / 360 if es.taste else 0.33
            luminosity = 0.9 - food.energy * 0.004 if food.energy > 20 else 0.82

            color = colorsys.hls_to_rgb(hue, luminosity, 1)

            ax.add_patch(Rectangle((food.position[0], food.position[1]), 1, 1, facecolor=color, linewidth=0))

        for bug in world.organism_lists['bug']['alive']:  # draw bugs
            bug_size = bug.energy * 0.01
            if bug_size < 0.3:
                bug_size = 0.3
            elif bug_size > 1.0:
                bug_size = 1.0

            if es.taste:  # black outline
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size, height=bug_size,
                                     facecolor='k', linewidth=0))
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size / 1.5,
                                     height=bug_size / 1.5,
                                     facecolor=colorsys.hls_to_rgb(float(bug.taste) / 360, 0.5, 1), linewidth=0))
            else:  # no outline
                ax.add_patch(Ellipse(xy=(bug.position[0] + 0.5, bug.position[1] + 0.5), width=bug_size, height=bug_size,
                                     facecolor='r', linewidth=0))

        ax.set_xticks(np.arange(0, world.columns + 1, 1))
        ax.set_yticks(np.arange(0, world.rows + 1, 1))
        # Turn off tick labels
        ax.set_yticklabels([])
        ax.set_xticklabels([])

        plt.title('time=%s' % world.time, fontsize=30)
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

    def plot_world_data(self, world=False, start=0):
        """
        Read the CSV (comma-separated values) output and plot the world and/or gene values for each time.
        world: set to True to plot the world.
        start: set a time to start plotting from, starts from 0 by default.
        """

        # settings for the world plot
        settings_file = csv.DictReader(open(os.path.join('data', self.seed, 'data_files', self.seed + '.csv')))
        for row in settings_file:
            row.pop('', None)
            row['columns'], row['rows'] = float(row['columns']), float(row['rows'])
            settings = row

        if settings['taste_evo'] == 'True':
            for path in ['food_gene_space', 'bug_gene_space']:
                if not os.path.exists(os.path.join('data', self.seed, path)):
                    os.makedirs(os.path.join('data', self.seed, path))

        else:
            if settings['food_rep_thresh_evo'] == 'True':
                if not os.path.exists(os.path.join('data', self.seed, 'food_rep_thresh_evo')):
                    os.makedirs(os.path.join('data', self.seed, 'food_rep_thresh_evo'))
            if settings['bug_rep_thresh_evo'] == 'True':
                if not os.path.exists(os.path.join('data', self.seed, 'bug_rep_thresh_evo')):
                    os.makedirs(os.path.join('data', self.seed, 'bug_rep_thresh_evo'))

        # create the list of organisms for each day
        world_file = csv.reader(open(os.path.join('data', self.seed, 'data_files', 'world_data.csv')), delimiter=',')

        organism_list = []
        for row in world_file:
            row.remove(row[-1])  # remove the '\n' for CSV files
            organism_list.append(row)

        organism_list = [[[float(organism[i]) if i > 0 else organism[i] for i in range(len(organism))]
                          for organism in day] for day in split_list(organism_list)]

        for _ in range(start):
            del organism_list[0]

        for i, day in enumerate(organism_list):  # loop through each day

            sys.stdout.write(
                '\r' + 'plotting world data, time: %r' % (i + start) + '/%r' % (len(organism_list) + start - 1) + '...')
            sys.stdout.flush()

            # plot the world
            if world:

                ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)

                for organism in day:

                    if organism[0] == "'food'":  # draw food
                        hue = organism[5] / 360 if settings['taste_evo'] == 'True' else 0.33
                        luminosity = 0.9 - organism[3] * 0.004 if organism[3] > 20 else 0.82

                        color = colorsys.hls_to_rgb(hue, luminosity, 1)

                        ax.add_patch(
                            Rectangle((organism[1], organism[2]), 1, 1, facecolor=color, linewidth=0))

                    elif organism[0] == "'bug'":  # draw bugs
                        bug_size = organism[3] * 0.01
                        if bug_size < 0.3:
                            bug_size = 0.3
                        elif bug_size > 1.0:
                            bug_size = 1.0

                        if settings['taste_evo'] == 'True':  # black outline
                            ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=bug_size,
                                                 height=bug_size, facecolor='k', linewidth=0))
                            ax.add_patch(
                                Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=bug_size / 1.5,
                                        height=bug_size / 1.5, facecolor=colorsys.hls_to_rgb(organism[5] / 360, 0.5, 1),
                                        linewidth=0))
                        else:  # no outline
                            ax.add_patch(Ellipse(xy=(organism[1] + 0.5, organism[2] + 0.5), width=bug_size,
                                                 height=bug_size, facecolor='r', linewidth=0))

                ax.set_xticks(np.arange(0, settings['columns'] + 1, 1))
                ax.set_yticks(np.arange(0, settings['rows'] + 1, 1))
                # Turn off tick labels
                ax.set_yticklabels([])
                ax.set_xticklabels([])

                plt.title('time=%s' % (i + start), fontsize=30)
                plt.savefig(os.path.join('data', self.seed, 'world', '%s.png' % (i + start)))
                plt.close()

            # plot genes
            if settings['food_rep_thresh_evo'] or settings['bug_rep_thresh_evo'] or settings['taste_evo'] == 'True':

                # create lists of food and bug gene data for plotting
                food_list = []
                bug_list = []

                for organism in day:
                    if organism[0] == "'food'":
                        food_list.append(organism)
                    elif organism[0] == "'bug'":
                        bug_list.append(organism)

                data_to_plot = [{'data': food_list, 'path': 'food_rep_thresh_evo', 'colour': 'g',
                                 'colour_maps': 'Greens', 'path2': 'food_gene_space'},
                                {'data': bug_list, 'path': 'bug_rep_thresh_evo', 'colour': 'r',
                                 'colour_maps': 'Reds', 'path2': 'bug_gene_space'}]

                for organism_data in data_to_plot:  # for each food and bug

                    # 2D Plot (heat map)
                    if settings['taste_evo'] == 'True':

                        # create lists of gene data
                        rep_thresh = []
                        taste = []

                        for organism in organism_data['data']:
                            rep_thresh.append(organism[4])
                            taste.append(organism[5])

                        # create and set co-ordinate values in gene space
                        x = [j for j in range(51)]  # create binned co-ordinate values
                        y = [j for j in range(61)]

                        rep_thresh = [int(j / 2) for j in rep_thresh]  # bin values
                        taste = [int(j / 6) for j in taste]

                        z = [[0 for _ in range(len(x))] for _ in range(len(y))]
                        z_list = [list(j) for j in zip(rep_thresh, taste)]  # set co-ordinate values

                        for coordinates in z_list:
                            z[coordinates[1]][coordinates[0]] += 1 / len(z_list)  # list of population frequencies

                        x = [j * 2 for j in x]  # expand binned data to fit plot
                        y = [j * 6 for j in y]

                        xi, yi = np.meshgrid(x, y)
                        zi = np.array(z)

                        plt.pcolormesh(xi, yi, zi, cmap=organism_data['colour_maps'])
                        plt.colorbar()
                        plt.xlim(0, 101)
                        plt.ylim(0, 359)
                        plt.xlabel('Reproduction Threshold')
                        plt.ylabel('Taste')
                        plt.title('time=%s' % (i + start))
                        plt.savefig(os.path.join('data', self.seed, organism_data['path2'], '%s.png' % (i + start)))
                        plt.close()

                    else:

                        # 1D Plot (bar chart)
                        if settings[organism_data['path']] == 'True':

                            rep_dict = {j: 0 for j in range(101)}

                            for organism in organism_data['data']:
                                # count number of occurrences of each reproduction threshold
                                rep_dict[organism[4]] += 1

                            y_pos = np.arange(len(rep_dict.keys()))  # set centre values for bars
                            total = sum(rep_dict.values())
                            if total > 0:
                                for key, value in rep_dict.items():
                                    rep_dict[key] = value / total  # normalisation

                            plt.bar(y_pos, rep_dict.values(), align='center', color=organism_data['colour'])
                            plt.xlabel('Reproduction Threshold')
                            plt.ylabel('Population')
                            plt.title('time=%s' % (i + start))
                            plt.savefig(os.path.join('data', self.seed, organism_data['path'], '%s.png' % (i + start)))
                            plt.close()
