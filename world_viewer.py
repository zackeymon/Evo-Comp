import os
import sys
import csv
import colorsys
from matplotlib import pyplot as plt
from matplotlib import collections as col
from constants import *
from utility_methods import *
import config as cfg


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

        # World plotting axis initialisation
        self.ax = plt.figure(figsize=(cfg.fig_size, cfg.fig_size)).add_subplot(1, 1, 1)
        self.ax.set_xlim(0, cfg.world['settings']['columns'])
        self.ax.set_ylim(0, cfg.world['settings']['rows'])
        # Turn off axis labels
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)

    def view_world(self, world):
        """"Plot the world: rectangles=food, circles=bugs"""

        # Food parameters for plotting
        if world.organism_lists[FOOD_NAME]['alive']:
            food_x_offsets, food_y_offsets, food_facecolors = ([] for _ in range(3))

            for food in world.organism_lists[FOOD_NAME]['alive']:
                hue = float(food.taste) / 360 if cfg.food['evolve_taste'] else 0.33
                luminosity = 0.9 - food.energy * 0.004 if food.energy > 20 else 0.82

                food_x_offsets.append(food.position[0] + 0.5)
                food_y_offsets.append(food.position[1] + 0.5)
                food_facecolors.append(
                    'k') if cfg.check_newly_spawned_plants and food.lifetime == 1 else food_facecolors.append(
                    colorsys.hls_to_rgb(hue, luminosity, 1))

            # Add final parameters, and create and plot collection
            food_sizes = np.full(len(food_x_offsets), (
                (cfg.fig_size * 1e5) / (cfg.world['settings']['columns'] * cfg.world['settings']['rows'])),
                                 dtype=np.int)
            food_linewidths = np.zeros(len(food_x_offsets))
            food_collection = col.RegularPolyCollection(4, rotation=np.pi / 4, sizes=food_sizes,
                                                        offsets=list(zip(food_x_offsets, food_y_offsets)),
                                                        transOffset=self.ax.transData, facecolors=food_facecolors,
                                                        linewidths=food_linewidths)
            self.ax.add_collection(food_collection)

        # Bug parameters for plotting
        if world.organism_lists[BUG_NAME]['alive']:
            bug_widths, bug_heights, bug_x_offsets, bug_y_offsets, bug_facecolors = ([] for _ in range(5))

            for bug in world.organism_lists[BUG_NAME]['alive']:

                bug_size = bug.energy * 0.01
                if bug_size < 0.3:
                    bug_size = 0.3
                elif bug_size > 1.0:
                    bug_size = 1.0

                bug_widths.append(bug_size)
                bug_heights.append(bug_size)
                bug_x_offsets.append(bug.position[0] + 0.5)
                bug_y_offsets.append(bug.position[1] + 0.5)

                if cfg.bug['evolve_taste']:  # black outline with coloured dot in centre
                    bug_facecolors.append('k')

                    bug_widths.append(bug_size / 1.5)
                    bug_heights.append(bug_size / 1.5)
                    bug_x_offsets.append(bug.position[0] + 0.5)
                    bug_y_offsets.append(bug.position[1] + 0.5)
                    bug_facecolors.append(
                        'k') if cfg.check_newly_spawned_bugs and bug.lifetime == 1 else bug_facecolors.append(
                        colorsys.hls_to_rgb(float(bug.taste) / 360, 0.5, 1))

                else:  # no outline
                    bug_facecolors.append(
                        'k') if cfg.check_newly_spawned_bugs and bug.lifetime == 1 else bug_facecolors.append('r')

            # Add final parameters, and create and plot collection
            bug_angles = np.zeros(len(bug_widths))
            bug_linewidths = np.zeros(len(bug_widths))
            bug_collection = col.EllipseCollection(bug_widths, bug_heights, bug_angles, units='xy',
                                                   offsets=list(zip(bug_x_offsets, bug_y_offsets)),
                                                   transOffset=self.ax.transData, facecolors=bug_facecolors,
                                                   linewidths=bug_linewidths)
            self.ax.add_collection(bug_collection)

        plt.title('time=%s' % world.time, fontsize=30)
        plt.savefig(os.path.join('data', world.seed, 'world', '%s.png' % world.time))
        plt.cla()

    def plot_world_stats(self):
        """Read the CSV (comma-separated values) output and plot trends."""

        print('reading world statistics...')

        if not os.path.exists(os.path.join('data', self.seed, 'world_statistics')):
            os.makedirs(os.path.join('data', self.seed, 'world_statistics'))

        data = [(np.genfromtxt(os.path.join('data', self.seed, 'data_files', path + '.csv'), delimiter=',',
                               names=['time', 'energy', 'population', 'dead_population', 'average_alive_lifetime',
                                      'average_lifespan', 'average_reproduction_threshold'])) for path in
                ['food_data', 'bug_data']]
        food_data, bug_data = data[0], data[1]

        data_to_plot = []
        time = food_data['time']

        data1 = [(food_data['population'], 'Alive'), (food_data['dead_population'], 'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data1, 'x_label': 'Time', 'y_label': 'Number of Food', 'title': 'Food Populations',
                             'filename': 'food_population.png'})

        data2 = [(bug_data['population'], 'Alive'), (bug_data['dead_population'], 'Deaths (last 10 cycles)')]
        data_to_plot.append({'data': data2, 'x_label': 'Time', 'y_label': 'Number of Bugs', 'title': 'Bug Populations',
                             'filename': 'bug_population.png'})

        data3 = [(food_data['energy'], 'Alive')]
        data_to_plot.append({'data': data3, 'x_label': 'Time', 'y_label': 'Energy', 'title': 'Food Energy',
                             'filename': 'food_energy.png'})

        data4 = [(bug_data['energy'], 'Alive')]
        data_to_plot.append({'data': data4, 'x_label': 'Time', 'y_label': 'Energy', 'title': 'Bug Energy',
                             'filename': 'bug_energy.png'})

        data5 = [(food_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (food_data['average_lifespan'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data5, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Food Lifetimes',
                             'filename': 'food_lifetime.png'})

        data6 = [(bug_data['average_alive_lifetime'], 'Average Alive Lifetime'),
                 (bug_data['average_lifespan'], 'Average Lifespan (last 10 cycles)')]
        data_to_plot.append({'data': data6, 'x_label': 'Time', 'y_label': 'Lifetime', 'title': 'Bug Lifetimes',
                             'filename': 'bug_lifetime.png'})

        data7 = [(food_data['average_reproduction_threshold'], 'Alive')]
        data_to_plot.append({'data': data7, 'x_label': 'Time', 'y_label': 'Reproduction Threshold',
                             'title': 'Food Reproduction Threshold', 'filename': 'food_reproduction_threshold.png'})

        data8 = [(bug_data['average_reproduction_threshold'], 'Alive')]
        data_to_plot.append({'data': data8, 'x_label': 'Time', 'y_label': 'Reproduction Threshold',
                             'title': 'Bug Reproduction Threshold', 'filename': 'bug_reproduction_threshold.png'})

        data9 = [(food_data['population'], 'Food'), (bug_data['population'], 'Bugs'),
                 (food_data['population'] + bug_data['population'], 'Food + Bugs')]
        data_to_plot.append({'data': data9, 'x_label': 'Time', 'y_label': 'Number', 'title': 'World Population',
                             'filename': 'world_population.png'})

        data10 = [(food_data['energy'], 'Food'), (bug_data['energy'], 'Bugs'),
                  (food_data['energy'] + bug_data['energy'], 'Food + Bugs')]
        data_to_plot.append({'data': data10, 'x_label': 'Time', 'y_label': 'Energy', 'title': 'World Energy',
                             'filename': 'world_energy.png'})

        print('plotting world statistics...')

        for data_dict in data_to_plot:
            plt.figure()
            for (y, l) in data_dict['data']:
                plt.plot(time, y, label=l)
            plt.xlabel(data_dict['x_label'])
            plt.ylabel(data_dict['y_label'])
            plt.legend()
            plt.title(data_dict['title'])
            plt.savefig(os.path.join('data', self.seed, 'world_statistics', data_dict['filename']))
            plt.close()

    def plot_world_data(self, world=False, start=0):
        """
        Read the CSV (comma-separated values) output and plot the world and/or gene values for each time.
        world: set to True to plot the world.
        start: set a time to start plotting from, starts from 0 by default.
        """

        if world or cfg.food['evolve_reproduction_threshold'] or cfg.food['evolve_taste'] or \
                cfg.bug['evolve_reproduction_threshold'] or cfg.bug['evolve_taste']:

            print('reading world data...')

            # Create output directories
            for switch in ['evolve_reproduction_threshold', 'evolve_taste']:
                if cfg.food[switch]:
                    if not os.path.exists(os.path.join('data', self.seed, 'food_' + str(switch.replace("'", "")))):
                        os.makedirs(os.path.join('data', self.seed, 'food_' + str(switch.replace("'", ""))))
                if cfg.bug[switch]:
                    if not os.path.exists(os.path.join('data', self.seed, 'bug_' + str(switch.replace("'", "")))):
                        os.makedirs(os.path.join('data', self.seed, 'bug_' + str(switch.replace("'", ""))))

            # Create the list of organisms for each day
            world_file = csv.reader(open(os.path.join('data', self.seed, 'data_files', 'world_data.csv')),
                                    delimiter=',')

            organism_list = []
            for row in world_file:
                row.remove(row[-1])  # remove the '\n' for CSV files
                organism_list.append(row)

            organism_list = [[[float(organism[i]) if i > 0 else organism[i] for i in range(len(organism))]
                              for organism in day] for day in split_list(organism_list)]

            for _ in range(start):
                del organism_list[0]

        # Plot the world
        if world:
            for i, day in enumerate(organism_list):  # loop through each day

                sys.stdout.write(
                    '\r' + 'plotting world data (world), time: %r' % (i + start) + '/%r' % (
                        len(organism_list) + start - 1) + '...')
                sys.stdout.flush()

                food_x_offsets, food_y_offsets, food_facecolors = ([] for _ in range(3))
                bug_widths, bug_heights, bug_x_offsets, bug_y_offsets, bug_facecolors = ([] for _ in range(5))

                for organism in day:

                    # Food parameters for plotting
                    if organism[0] == "'food'":
                        hue = float(organism[5]) / 360 if cfg.food['evolve_taste'] else 0.33
                        luminosity = 0.9 - organism[3] * 0.004 if organism[3] > 20 else 0.82

                        food_x_offsets.append(organism[1] + 0.5)
                        food_y_offsets.append(organism[2] + 0.5)
                        food_facecolors.append(colorsys.hls_to_rgb(hue, luminosity, 1))

                    # Bug parameters for plotting
                    elif organism[0] == "'bug'":

                        bug_size = organism[3] * 0.01
                        if bug_size < 0.3:
                            bug_size = 0.3
                        elif bug_size > 1.0:
                            bug_size = 1.0

                        bug_widths.append(bug_size)
                        bug_heights.append(bug_size)
                        bug_x_offsets.append(organism[1] + 0.5)
                        bug_y_offsets.append(organism[2] + 0.5)

                        if cfg.bug['evolve_taste']:  # black outline with coloured dot in centre
                            bug_facecolors.append('k')

                            bug_widths.append(bug_size / 1.5)
                            bug_heights.append(bug_size / 1.5)
                            bug_x_offsets.append(organism[1] + 0.5)
                            bug_y_offsets.append(organism[2] + 0.5)
                            bug_facecolors.append(colorsys.hls_to_rgb(float(organism[5]) / 360, 0.5, 1))

                        else:  # no outline
                            bug_facecolors.append('r')

                # Add final parameters
                food_sizes = np.full(len(food_x_offsets), (
                    (cfg.fig_size * 1e5) / (cfg.world['settings']['columns'] * cfg.world['settings']['rows'])),
                                     dtype=np.int)
                food_linewidths = np.zeros(len(food_x_offsets))
                bug_angles = np.zeros(len(bug_widths))
                bug_linewidths = np.zeros(len(bug_widths))

                # Create and plot collections
                if food_x_offsets:
                    food_collection = col.RegularPolyCollection(4, rotation=np.pi / 4, sizes=food_sizes,
                                                                offsets=list(zip(food_x_offsets, food_y_offsets)),
                                                                transOffset=self.ax.transData,
                                                                facecolors=food_facecolors,
                                                                linewidths=food_linewidths)
                    self.ax.add_collection(food_collection)
                if bug_widths:
                    bug_collection = col.EllipseCollection(bug_widths, bug_heights, bug_angles, units='xy',
                                                           offsets=list(zip(bug_x_offsets, bug_y_offsets)),
                                                           transOffset=self.ax.transData, facecolors=bug_facecolors,
                                                           linewidths=bug_linewidths)
                    self.ax.add_collection(bug_collection)

                plt.title('time=%s' % (i + start), fontsize=30)
                plt.savefig(os.path.join('data', self.seed, 'world', '%s.png' % (i + start)))
                plt.cla()

            sys.stdout.write('\n')  # write gene data outputs on a new line

        # Plot genes
        if cfg.food['evolve_reproduction_threshold'] or cfg.food['evolve_taste'] or \
                cfg.bug['evolve_reproduction_threshold'] or cfg.bug['evolve_taste']:
            for i, day in enumerate(organism_list):  # loop through each day

                sys.stdout.write(
                    '\r' + 'plotting world data (genes), time: %r' % (i + start) + '/%r' % (
                        len(organism_list) + start - 1) + '...')
                sys.stdout.flush()

                # Create lists of food and bug gene data for plotting
                food_list, bug_list = [], []

                for organism in day:
                    if organism[0] == "'food'":
                        food_list.append(organism)
                    elif organism[0] == "'bug'":
                        bug_list.append(organism)

                data_to_plot = [
                    {'data': food_list, 'switch': cfg.food, 'path': 'food_evolve_reproduction_threshold', 'colour': 'g',
                     'path2': 'food_evolve_taste', 'colour_maps': 'Greens'},
                    {'data': bug_list, 'switch': cfg.bug, 'path': 'bug_evolve_reproduction_threshold', 'colour': 'r',
                     'path2': 'bug_evolve_taste', 'colour_maps': 'Reds'}]

                for organism_data in data_to_plot:  # for food and bugs

                    rep_thresh = [organism[4] for organism in organism_data['data']]
                    max_rep_thresh = int(max(rep_thresh)) if rep_thresh else 0

                    # 1D Plot (bar chart)
                    if organism_data['switch']['evolve_reproduction_threshold']:

                        # Reproduction threshold dictionary sets axis plot range
                        rep_dict = {j: 0 for j in range(101)} if max_rep_thresh <= 100 else {j: 0 for j in
                                                                                             range(max_rep_thresh + 1)}

                        for organism in organism_data['data']:
                            # Count number of occurrences of each reproduction threshold
                            rep_dict[organism[4]] += 1

                        y_pos = np.arange(len(rep_dict.keys()))  # set centre values for bars
                        total = sum(rep_dict.values())
                        if total > 0:
                            for key, value in rep_dict.items():
                                rep_dict[key] = value / total  # normalisation

                        plt.figure()
                        plt.bar(y_pos, rep_dict.values(), align='center', color=organism_data['colour'])
                        if not rep_thresh:
                            plt.ylim(0, 1)
                        plt.xlabel('Reproduction Threshold')
                        plt.ylabel('Population')
                        plt.title('time=%s' % (i + start))
                        plt.savefig(os.path.join('data', self.seed, organism_data['path'], '%s.png' % (i + start)))
                        plt.close()

                    # 2D Plot (heat map)
                    if organism_data['switch']['evolve_taste']:

                        # Create lists of gene data
                        taste = [organism[5] for organism in organism_data['data']]

                        # Create and set co-ordinate values in gene space
                        x = [j for j in range(51)] if max_rep_thresh <= 100 else [j for j in
                                                                                  range((int(max_rep_thresh / 2) + 1))]
                        y = [j for j in range(61)]

                        rep_thresh = [int(j / 2) for j in rep_thresh]  # bin values into binned co-ordinate values
                        taste = [int(j / 6) for j in taste]

                        z = [[0 for _ in range(len(x))] for _ in range(len(y))]
                        z_list = [list(j) for j in zip(rep_thresh, taste)]  # set co-ordinate values

                        for coordinates in z_list:
                            z[coordinates[1]][coordinates[0]] += 1 / len(z_list)  # list of population frequencies

                        x = [j * 2 for j in x]  # expand binned data to fit plot
                        y = [j * 6 for j in y]

                        xi, yi = np.meshgrid(x, y)
                        zi = np.array(z)

                        plt.figure()
                        plt.pcolormesh(xi, yi, zi, cmap=organism_data['colour_maps'])
                        plt.colorbar()
                        plt.xlim(0, 100) if max_rep_thresh <= 100 else plt.xlim(0, max_rep_thresh)
                        plt.ylim(0, 360)
                        plt.xlabel('Reproduction Threshold')
                        plt.ylabel('Taste')
                        plt.title('time=%s' % (i + start))
                        plt.savefig(os.path.join('data', self.seed, organism_data['path2'], '%s.png' % (i + start)))
                        plt.close()
