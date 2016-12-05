import numpy as np
import os
from collections import OrderedDict
from matplotlib import pyplot as plt


class GeneViewer:
    """
    A class to output the data for genes and to plot them in gene space.
    """

    def __init__(self, world):
        """
        Gene Viewer Initialisation
        :param world: The world being viewed
        """
        self.world = world
        self.food_taste_average = 0.0
        self.food_gene_data, self.bug_gene_data = (OrderedDict
                                                   ([('reproduction_threshold', []),
                                                     ('taste', [])])
                                                   for _ in range(2))

    @staticmethod
    def split_list(data):
        """Split the overall list of data into separate days."""
        data[np.isnan(data)] = -1
        split_data = []
        for item in data:
            if item == -1:
                split_data.append([])
            else:
                split_data[-1].append(int(item))

        data = split_data

        return data

    def generate_gene_data(self):
        """Add data for genes for the current world iteration to a list."""

        data_to_generate = [{'data': self.food_gene_data, 'list': self.world.food_list},
                            {'data': self.bug_gene_data, 'list': self.world.bug_list}]
        food_taste_list = []

        for i, organism_type in enumerate(data_to_generate):
            organism_type['data']['reproduction_threshold'].append('time=%r' % self.world.time)
            organism_type['data']['taste'].append(None)
            for organism in organism_type['list']:
                organism_type['data']['reproduction_threshold'].append(organism.reproduction_threshold)
                organism_type['data']['taste'].append(organism.taste)

                if i == 0:
                    if organism.taste >= 180:
                        food_taste_list.append(organism.taste - 360)
                    else:
                        food_taste_list.append(organism.taste)

        self.food_taste_average = np.average(food_taste_list)

        # NaN != NaN
        if self.food_taste_average != self.food_taste_average:
            self.food_taste_average = 0.0

    def output_gene_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        data_to_output = [{'data': self.food_gene_data.values(), 'path': 'food_gene_data'},
                          {'data': self.bug_gene_data.values(), 'path': 'bug_gene_data'}]

        for organism_type in data_to_output:
            with open(os.path.join('data', self.world.seed, 'data_files',
                                   organism_type['path'] + '.csv'), 'a') as organism_gene_file:
                for reproduction_threshold, taste in zip(*organism_type['data']):
                    organism_gene_file.write('%r,' % reproduction_threshold + '%r,' % taste + '\n')

    def plot_gene_data(self):
        """Read the CSV (comma-separated values) output and plot in gene space."""

        food_gene_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'food_gene_data.csv'),
                                       delimiter=',', names=['reproduction_threshold', 'taste'])

        bug_gene_data = np.genfromtxt(os.path.join('data', self.world.seed, 'data_files', 'bug_gene_data.csv'),
                                      delimiter=',', names=['reproduction_threshold', 'taste'])

        for k, organism_data in enumerate([food_gene_data, bug_gene_data]):

            # 1D Plot (bar chart)
            for i, day in enumerate(self.split_list(organism_data['reproduction_threshold'])):
                rep_dict = {j: 0 for j in range(101)}

                for rep_thresh in day:
                    # count number of occurrences of each reproduction threshold for each time
                    rep_dict[rep_thresh] += 1

                y_pos = np.arange(len(rep_dict.keys()))
                total = sum(rep_dict.values())
                if total > 0:
                    for key, value in rep_dict.items():
                        rep_dict[key] = value / total  # normalisation

                plt.figure()
                plt.xlabel('Reproduction Threshold')
                plt.ylabel('Population')
                plt.title('time=%s' % i)

                if k == 0:
                    plt.bar(y_pos, rep_dict.values(), align='center', color='g')
                    plt.savefig(os.path.join('data', self.world.seed, 'food_gene_data', '%s.png' % i))
                    plt.close()

                elif k == 1:
                    plt.bar(y_pos, rep_dict.values(), align='center', color='r')
                    plt.savefig(os.path.join('data', self.world.seed, 'bug_gene_data', '%s.png' % i))
                    plt.close()

            # 2D Plot (heat map)
            for i in range(self.world.time):
                rep_thresh = self.split_list(organism_data['reproduction_threshold'])[i]
                taste = self.split_list(organism_data['taste'])[i]

                x = [i for i in range(52)]
                y = [i for i in range(61)]

                rep_thresh = [int(j / 2) for j in rep_thresh]  # bin food
                taste = [int(j / 6) for j in taste]

                z = [[0 for _ in range(len(x))] for _ in range(len(y))]
                z_list = [list(i) for i in zip(rep_thresh, taste)]

                for value in z_list:
                    z[value[1]][value[0]] += 1 / len(z_list)  # list of population frequencies

                x = [j * 2 for j in x]
                y = [j * 6 for j in y]

                xi, yi = np.meshgrid(x, y)
                zi = np.array(z)

                plt.figure()
                plt.xlim(0, 101)
                plt.ylim(0, 359)
                plt.xlabel('Reproduction Threshold')
                plt.ylabel('Taste')
                plt.title('time=%s' % i)

                if k == 0:
                    plt.pcolormesh(xi, yi, zi, cmap='Greens')
                    plt.colorbar()
                    plt.savefig(os.path.join('data', self.world.seed, 'food_gene_space', '%s.png' % i))
                    plt.close()

                elif k == 1:
                    plt.pcolormesh(xi, yi, zi, cmap='Reds')
                    plt.colorbar()
                    plt.savefig(os.path.join('data', self.world.seed, 'bug_gene_space', '%s.png' % i))
                    plt.close()
