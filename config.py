"""
Initialisation Settings
"""

# Plotting
fig_size = 20  # pixel size is fig_size x dpi
save_world_view = True
check_newly_spawned_plants = True
check_newly_spawned_bugs = False

world = dict(
    settings=dict(
        seed='rt0_t0-cs_L-002_NEWWWW',
        rows=100,
        columns=100,
        fertile_lands=None,
        init_food=500,
        init_bugs=100
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=30,
        energy_max=100
        # TODO: food & bug taste
    ),
    bug_spawn_vals=dict(
        energy=20,
        reproduction_threshold=60,
        energy_max=100
    )
)

food_endangered_threshold = 100
bug_endangered_threshold = 50

food_over_shadow = True
food_over_shadow_ratio = 0.8

food = dict(
    growth_rate=3,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)

bug = dict(
    respiration_rate=4,
    eat_tax=2,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)
