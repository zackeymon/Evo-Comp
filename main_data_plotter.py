"""
Copy config.py file from (seeded) folder of world to view.
"""

from world_viewer import WorldViewer

world_viewer = WorldViewer('rt0_t0-rs_L-001')  # seed of world to view

world_viewer.plot_world_stats()
world_viewer.plot_world_data()
