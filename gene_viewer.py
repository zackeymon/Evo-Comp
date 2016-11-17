import numpy as np
import os
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

        if not os.path.exists(os.path.join('data', self.world.seed)):
            os.makedirs(os.path.join('data', self.world.seed))

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

        self.world.bug_gene_data['reproduction_threshold'].append('time=%r' % self.world.time)
        self.world.bug_gene_data['evolutionary_trait'].append(None)
        for bug in self.world.bug_list:
            self.world.bug_gene_data['reproduction_threshold'].append(bug.reproduction_threshold)
            self.world.bug_gene_data['evolutionary_trait'].append(None)

    def output_gene_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.world.seed, 'bug_gene_data.csv'), 'a') as bug_gene_file:
            for evolutionary_trait, reproduction_threshold in zip(*self.world.bug_gene_data.values()):
                bug_gene_file.write('%r,' % evolutionary_trait + '%r,' % reproduction_threshold + '\n')

    def plot_gene_data(self):
        """Read the CSV (comma-separated values) output and plot in gene space."""

        gene_data = np.genfromtxt(os.path.join('data', self.world.seed, 'bug_gene_data.csv'), delimiter=',',
                                  names=['reproduction_threshold', 'evolutionary_trait'])

        # 1D Plot (bar chart)
        for i, day in enumerate(self.split_list(gene_data['reproduction_threshold'])):
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
            plt.savefig(os.path.join('data', self.world.seed, 'gene_data_%s.png' % i))
            plt.close()
