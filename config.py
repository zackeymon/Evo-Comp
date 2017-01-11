"""
Initialisation Settings
"""

# Plotting
fig_size = 20  # pixel size is fig_size x dpi
save_world_view = False
check_newly_spawned_plants = False
check_newly_spawned_bugs = False

world = dict(
    settings=dict(
        seed='K40000_rt30_gr2_001',
        rows=200,
        columns=200,
        fertile_lands=None,
        init_food=100,
        init_bugs=0
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=30,
        energy_max=100
        # TODO: food & bug taste
    ),
    bug_spawn_vals=dict(
        energy=20,
        reproduction_threshold=70,
        energy_max=100
    )
)

# World parameters
food_endangered_threshold = 0
bug_endangered_threshold = 0
food_min_energy = 0
bug_min_energy = 0

# Food parameters
food_maturity_age = 1
food_reproduction_cost = 0

food = dict(
    growth_rate=2,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)

# Bug parameters
bug_maturity_age = 1
bug_mouse_size = 60
bug_reproduction_cost = 0

bug = dict(
    respiration_rate=2,
    eat_tax=0,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)
