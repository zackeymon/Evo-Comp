"""
Copy config.py file from (seeded) folder of world to view.
"""

from world_viewer import WorldViewer

world_viewer = WorldViewer('rt0_t0-128-gr10')  # seed of world to view

# world_viewer.plot_world_stats()
world_viewer.plot_world_data(day=100, world=True)  # plot that day
