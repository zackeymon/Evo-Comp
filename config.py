"""
Initialisation Settings
"""

# Plotting
fig_size = 20  # pixel size is fig_size x dpi
save_world_view_every_day = False
check_newly_spawned_plants = False  # for debugging
check_newly_spawned_bugs = False

# World set up
world = dict(
    settings=dict(
        seed='rt0_t0-128-gr10',  # set to None to use current datetime as seed
        rows=128,
        columns=128,
        fertile_lands=None,  # fertile_lands=[[[20, 20], [29, 29]], [[50, 20], [59, 29]], [[20, 50], [29, 59]]])
        init_food=100,
        init_bugs=10
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=30,
        energy_max=100,
        taste=180

    ),
    bug_spawn_vals=dict(
        energy=30,
        reproduction_threshold=70,
        energy_max=100,
        taste=180
    )
)

# World parameters
max_compatible_taste = 180  # scaling eat probability within range
offspring_energy_fraction = 0.5
endangered_time = 300  # time up to which spawn additional organisms if below endangered threshold
food_endangered_threshold = 100
bug_endangered_threshold = 10

food = dict(
    growth_rate=10,
    min_energy=10,
    maturity_age=1,
    reproduction_cost=1,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=True,
    taste_mutation_limit=5
)

bug = dict(
    respiration_rate=10,
    min_energy=0,
    maturity_age=1,
    reproduction_cost=6,

    eat_tax=0,
    mouth_size=40,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=True,
    taste_mutation_limit=5
)
