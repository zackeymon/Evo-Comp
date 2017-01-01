"""
Initialisation Settings
"""
save_world_view = False

world = dict(
    settings=dict(
        seed='rt0_t0-rs_XXL-001',
        rows=500,
        columns=500,
        fertile_lands=[[[100, 100], [400, 400]]],
        init_food=20000,
        init_bugs=1000
    ),
    food_spawn_vals=dict(
        energy=20,
        reproduction_threshold=24,
        energy_max=100
        # TODO: food & bug taste
    ),
    bug_spawn_vals=dict(
        energy=20,
        reproduction_threshold=50,
        energy_max=100
    )
)

food_endangered_threshold = 999999999
bug_endangered_threshold = 0

food = dict(
    growth_rate=4,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=10
)

bug = dict(
    respiration_rate=3,

    # Evolution switches
    evolve_reproduction_threshold=False,
    reproduction_threshold_mutation_limit=5,

    evolve_taste=False,
    taste_mutation_limit=10
)
