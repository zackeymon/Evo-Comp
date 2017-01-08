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
        seed='2017-01-08_18-37-26',
        rows=50,
        columns=50,
        fertile_lands=None,
        init_food=0,
        init_bugs=0
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=40,
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
food_endangered_threshold = 9999
bug_endangered_threshold = 2
food_min_energy = 0
bug_min_energy = 0

food_maturity_age = 1
food_reproduction_cost = 0

food = dict(
    growth_rate=1,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)

bug_maturity_age = 1
bug_mouse_size = 100
bug_reproduction_cost = 0

bug = dict(
    respiration_rate=1,
    eat_tax=0,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)
