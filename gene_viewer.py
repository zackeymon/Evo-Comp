import numpy as np
import os
import scipy.interpolate
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
        self.food_gene_average = 0
        self.food_gene_data = OrderedDict([('reproduction_threshold', []), ('gene_val', [])])
        self.bug_gene_data = OrderedDict([('reproduction_threshold', []), ('gene_val', [])])


    @staticmethod
    def split_list(data):
        data[np.isnan(data)] = -1
        split_data = []
        for item in data:
            if item == -1:
                split_data.append([])
            else:
                split_data[-1].append(item)

        data = split_data

        return data

    def generate_gene_data(self):
        """Add data for genes for the current world iteration to a list."""

        food_gene_val = []
        self.food_gene_data['reproduction_threshold'].append('time=%r' % self.world.time)
        self.food_gene_data['gene_val'].append(None)
        for food in self.world.food_list:
            self.food_gene_data['reproduction_threshold'].append(food.reproduction_threshold)
            self.food_gene_data['gene_val'].append(food.gene_val)
            gene_av = food.gene_val

            if food.gene_val >= 180:
                gene_av = food.gene_val - 360
            food_gene_val.append(gene_av)
        self.food_gene_average = np.average(food_gene_val)

        self.bug_gene_data['reproduction_threshold'].append('time=%r' % self.world.time)
        self.bug_gene_data['gene_val'].append(None)
        for bug in self.world.bug_list:
            self.bug_gene_data['reproduction_threshold'].append(bug.reproduction_threshold)
            self.bug_gene_data['gene_val'].append(bug.gene_val)

    def output_gene_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""
        
        with open(os.path.join('data', self.world.seed, 'food_gene_data', 'food_gene_data.csv'), 'a') as food_gene_file:
            for reproduction_threshold, gene_val in zip(*self.food_gene_data.values()):
                food_gene_file.write('%r,' % reproduction_threshold + '%r,' % gene_val + '\n')

        with open(os.path.join('data', self.world.seed, 'bug_gene_data', 'bug_gene_data.csv'), 'a') as bug_gene_file:
            for reproduction_threshold, gene_val in zip(*self.bug_gene_data.values()):
                bug_gene_file.write('%r,' % reproduction_threshold + '%r,' % gene_val + '\n')

    def plot_gene_data(self):
        """Read the CSV (comma-separated values) output and plot in gene space."""

        food_gene_data = np.genfromtxt(os.path.join('data', self.world.seed, 'food_gene_data', 'food_gene_data.csv'), delimiter=',',
                                       names=['reproduction_threshold', 'gene_val'])
        bug_gene_data = np.genfromtxt(os.path.join('data', self.world.seed, 'bug_gene_data', 'bug_gene_data.csv'), delimiter=',',
                                      names=['reproduction_threshold', 'gene_val'])

        # 1D Plot (bar chart)
        for i, day in enumerate(self.split_list(food_gene_data['reproduction_threshold'])):
            rep_dict = {j: 0 for j in range(101)}

            for rep_thresh in day:

                # count number of occurences of each reproduction threshold for each time
                rep_dict[int(rep_thresh)] += 1

            y_pos = np.arange(len(rep_dict.keys()))
            total = sum(rep_dict.values())
            if total > 0:
                for key, value in rep_dict.items():
                    rep_dict[key] = value / total

            plt.bar(y_pos, rep_dict.values(), align='center', color='red')
            plt.xlabel('Reproduction Threshold')
            plt.ylabel('Population')
            plt.title('time=%s' % i)
            plt.savefig(os.path.join('data', self.world.seed, 'food_gene_data', '%s.png' % i))
            plt.close()

        for i, day in enumerate(self.split_list(bug_gene_data['reproduction_threshold'])):
            rep_dict = {j: 0 for j in range(101)}

            for rep_thresh in day:

                # count number of occurences of each reproduction threshold for each time
                rep_dict[int(rep_thresh)] += 1

            y_pos = np.arange(len(rep_dict.keys()))
            total = sum(rep_dict.values())
            for key, value in rep_dict.items():
                rep_dict[key] = value / total

            plt.bar(y_pos, rep_dict.values(), align='center', color='red')
            plt.xlabel('Reproduction Threshold')
            plt.ylabel('Population')
            plt.title('time=%s' % i)
            plt.savefig(os.path.join('data', self.world.seed, 'bug_gene_data', '%s.png' % i))
            plt.close()
        
        # 2D plot(contours)
        for i in range(self.world.time):

            rep_thresh = self.split_list(food_gene_data['reproduction_threshold'])[i]
            gene_val = self.split_list(food_gene_data['gene_val'])[i]
            z_list = []
            for value in zip(rep_thresh, gene_val):
                z_list.append(value)

            data = OrderedDict([(x, z_list.count(x)) for x in z_list])
            old_z = [x for x in data.values()]
            total = sum(old_z)
            z = [x / total for x in old_z]

            trait_dict = OrderedDict.fromkeys(zip(rep_thresh, gene_val))
            x = [d[0] for d in trait_dict]
            y = [d[1] for d in trait_dict]

            xi, yi = np.linspace(0, 101, 101), np.linspace(0, 359, 359)
            xi, yi = np.meshgrid(xi, yi)

            if len(z) > 1:
                rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
                zi = rbf(xi, yi)
                plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower', aspect='auto')

            plt.scatter(x, y, c=z)
            plt.colorbar()
            plt.xlim(0, 101)
            plt.ylim(0, 359)
            plt.xlabel('Reproduction Threshold')
            plt.ylabel('Gene Value')
            plt.title('time=%s' % i)
            plt.savefig(os.path.join('data', self.world.seed, 'food_gene_space', '%s.png' % i))
            plt.close()

        for i in range(self.world.time):

            rep_thresh = self.split_list(bug_gene_data['reproduction_threshold'])[i]
            gene_val = self.split_list(bug_gene_data['gene_val'])[i]
            z_list = []
            for value in zip(rep_thresh, gene_val):
                z_list.append(value)

            data = OrderedDict([(x, z_list.count(x)) for x in z_list])
            old_z = [x for x in data.values()]
            total = sum(old_z)
            z = [x / total for x in old_z]

            trait_dict = OrderedDict.fromkeys(zip(rep_thresh, gene_val))
            x = [d[0] for d in trait_dict]
            y = [d[1] for d in trait_dict]

            xi, yi = np.linspace(0, 101, 101), np.linspace(0, 359, 359)
            xi, yi = np.meshgrid(xi, yi)

            if len(z) > 1:
                rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
                zi = rbf(xi, yi)
                plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower', aspect='auto')

            plt.scatter(x, y, c=z)
            plt.colorbar()
            plt.xlim(0, 101)
            plt.ylim(0, 359)
            plt.xlabel('Reproduction Threshold')
            plt.ylabel('Gene Value')
            plt.title('time=%s' % i)
            plt.savefig(os.path.join('data', self.world.seed, 'bug_gene_space', '%s.png' % i))
            plt.close()
