world = dict(
    settings=dict(
        seed=None,
        rows=100,
        columns=100,
        fertile_lands=None
    ),
    spawn_values=dict(
        food=dict(
            energy=20,
            reproduction_threshold=30,
            energy_max=100,
            # TODO: taste value
        ),
        bug=dict(
            energy=15,
            reproduction_threshold=70,
            energy_max=100,
        )
    )
)

food = dict(
    growth_rate=2,

    evolution_switches=dict(
        reproduction_threshold=True,
        taste=True
    )
)

bug = dict(
    respiration_rate=2,

    evolution_switches=dict(
        reproduction_threshold=True,
        taste=True
    )
)

food_reproduction_threshold = True
bug_reproduction_threshold = True
taste = True
