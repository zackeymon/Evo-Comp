"""
Initialisation Settings
"""

# Plotting
fig_size = 20  # pixel size is fig_size x dpi
save_world_view = True
check_newly_spawned_plants = False
check_newly_spawned_bugs = False

world = dict(
    settings=dict(
        seed='rt1_t0-large-001-mouth',
        rows=100,
        columns=100,
        fertile_lands=[[[10, 10], [89, 89]]],
        init_food=100,
        init_bugs=100
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=40,
        energy_max=100
        # TODO: food & bug taste
    ),
    bug_spawn_vals=dict(
        energy=30,
        reproduction_threshold=50,
        energy_max=100
    )
)

taste_range = 180  # scales within range

food_endangered_threshold = 100
bug_endangered_threshold = 10

food_min_energy = 10
food_maturity_age = 5
food_reproduction_cost = 6

food = dict(
    growth_rate=4,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)

bug_min_energy = 0
bug_maturity_age = 5
bug_mouse_size = 40
bug_reproduction_cost = 6


bug = dict(
    respiration_rate=6,
    eat_tax=0,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=5
)
