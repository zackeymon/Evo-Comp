"""
Initialisation Settings
"""

world = dict(
    settings=dict(
        seed=None,
        rows=100,
        columns=100,
        fertile_lands=None,
        init_food=500,
        init_bugs=50
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=25,
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

food = dict(
    growth_rate=2,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=10
)

bug = dict(
    respiration_rate=4,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=10
)
