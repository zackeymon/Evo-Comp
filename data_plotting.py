import random
from world import World
from world_viewer import WorldViewer
from gene_viewer import GeneViewer

myWorld = World(rows=50, columns=50, seed='2016-11-30_19-29-26')
myWorld.time = 146  # the last time value in bug_data or food_data
worldViewer = WorldViewer(myWorld)
geneViewer = GeneViewer(myWorld)

# worldViewer.plot_data()
# worldViewer.plot_world_data()
geneViewer.plot_gene_data()
