"""
Copy config.py file from (seeded) folder of world to view.
"""

from world_viewer import WorldViewer

world_viewer = WorldViewer('rt0_t0-128-gr1-01')  # seed of world to view

world_viewer.plot_world_stats()
world_viewer.plot_world_data(world=True, start=150)
