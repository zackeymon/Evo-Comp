import numpy as np
import os
import datetime
from matplotlib import pyplot as plt


# Do we need this class?
class GeneViewer:
    """
    A class to output the data for genes and to plot them in gene space.
    """
    def __init__(self, time_stamp=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')):
        """
        Gene Viewer Initialisation
        :param time_stamp: The beginning of time
        """
        self.time_stamp = time_stamp

        if not os.path.exists(os.path.join('data', self.time_stamp)):
            os.makedirs(os.path.join('data', self.time_stamp))

    @staticmethod
    def generate_gene_data(self, world):
        """Add data for genes for the current world iteration to a list."""

        world.bug_gene_data[0].append('time=%r' % world.time)
        world.bug_gene_data[1].append(None)
#       I could define a blank class here to use instead of None
        for bug in world.bugList:
            world.bug_gene_data[0].append(bug.reproduction_threshold)
            world.bug_gene_data[1].append(None)

    def output_gene_data(self, world):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.time_stamp, 'bug_gene_data.csv'), 'a') as bug_gene_file:
            for evolutionary_trait, reproduction_threshold in zip(*world.bug_gene_data):
                bug_gene_file.write('%r,' % evolutionary_trait + '%r,' % reproduction_threshold + '\n')

    def plot_gene_data(self):
        """Read the CSV (comma-separated values) output and plot as bar charts in gene space."""

        gene_data = np.genfromtxt(os.path.join('data', self.time_stamp, 'bug_gene_data.csv'), delimiter=',',
                                  names=['reproduction_threshold', 'trait'])

        gene_data['reproduction_threshold'][np.isnan(gene_data['reproduction_threshold'])] = -1

#       will turn this into a function later, splits into separate lists based on time
        split_gene_data = []
        for item in gene_data['reproduction_threshold']:
            if item == -1:
                split_gene_data.append([item])
            else:
                split_gene_data[-1].append(item)

#       remove value that allows for splitting lists
        for time_segment in split_gene_data:
            time_segment.remove(-1)

        for i in range(len(split_gene_data)):

#           count number of occurences of each reproduction threshold for each time
            for_plotting = {x: split_gene_data[i].count(x) for x in split_gene_data[i]}
            values, frequencies = for_plotting.keys(), for_plotting.values()
            sum_frequencies = sum(frequencies)
            for_plotting.update((x, y/sum_frequencies) for x, y in for_plotting.items())

#           bar chart
            y_pos = np.arange(len(values))

            plt.bar(y_pos, frequencies, align='center', color='red')
            plt.xticks(y_pos, values)
            plt.xlabel('Reproduction Threshold')
            plt.ylabel('Population')
            plt.title('time=%s' % i)
            plt.savefig(os.path.join('data', self.time_stamp, 'gene_data_%s.png' % i))
            plt.close()

            plt.show()

# either fill in missing values after dictionary is generated (prob best idea) or add before and somehow count as zero
