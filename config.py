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
        reproduction_threshold=30,
        energy_max=100
        # TODO: food & bug taste
    ),
    bug_spawn_vals=dict(
        energy=15,
        reproduction_threshold=70,
        energy_max=100
    )
)

food = dict(
    growth_rate=2,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=True,
    taste_mutation_limit=10
)

bug = dict(
    respiration_rate=2,

    # Evolution switches
    evolve_reproduction_threshold=True,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=True,
    taste_mutation_limit=10
)
