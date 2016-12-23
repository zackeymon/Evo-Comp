"""
Copy config.py file from (seeded) folder of world to view.
"""

from world_viewer import WorldViewer

world_viewer = WorldViewer('2016-12-08_17-38-04')  # seed of world to view

world_viewer.plot_world_stats()
world_viewer.plot_world_data(world=True)
