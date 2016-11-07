import os
import datetime


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

    def generate_gene_data(self, world):
        """Add data for genes for the current world iteration to a list."""

        world.bug_gene_data[0].append('time=%r' % world.time)
        world.bug_gene_data[1].append(None)
#       I could define a blank class here to use instead of None
        for bug in world.bugList:
            world.bug_gene_data[0].append(1)
            world.bug_gene_data[1].append(bug.reproduction_threshold)

    def output_gene_data(self, world):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.time_stamp, 'bug_gene_data.csv'), 'a') as bug_gene_file:
            for number_of_offspring, reproduction_threshold in zip(*world.bug_gene_data):
                bug_gene_file.write('%r,' % number_of_offspring + '%r,' % reproduction_threshold + '\n')

    def plot_gene_data(self):
        """Read the CSV (comma-separated values) output and plot as contours in gene space."""
