import random
from world import World
from world_viewer import WorldViewer
from gene_viewer import GeneViewer

myWorld = World(rows=30, columns=30, seed='2016-11-30_10-03-04')
worldViewer = WorldViewer(myWorld)
geneViewer = GeneViewer(myWorld)
random.seed('2016-11-30_10-03-04')

worldViewer.plot_data()
geneViewer.plot_gene_data()
