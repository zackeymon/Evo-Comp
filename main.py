import config as cfg
from constants import *
from direction import Direction
from kill_switch import KillSwitch
from world import World
from world_recorder import WorldRecorder
from world_viewer import WorldViewer


##################################
# --------Initialisation-------- #
##################################
# Create a new world
w = World(**cfg.world['settings'])

# Make a kill switch
KillSwitch.setup()

# Set up analysis classes
world_recorder = WorldRecorder(w)
world_viewer = WorldViewer(w.seed)

#######################
# --------Run-------- #
#######################
while KillSwitch.is_off():
    # Generate yesterday data
    world_recorder.generate_world_stats()
    world_recorder.generate_world_data()
    if cfg.save_world_view:
        world_viewer.view_world(w)

    # Prepare today's work
    alive_plants, alive_bugs = w.prepare_today()

    # Food life cycle
    plant_index = 0
    while plant_index < len(alive_plants):
        plant = alive_plants[plant_index]

        # Should it die?
        if plant.energy <= 0:
            w.kill(plant)
            continue

        plant.grow()

        # Can it reproduce?
        if plant.energy >= plant.reproduction_threshold and plant.lifetime > 1:
            trial_direction = Direction.random()

            if w.available(plant, trial_direction):
                w.spawn(plant.reproduce(trial_direction))
            else:
                # Try overshadow the original plant
                try:
                    defending_plant = w.plant_position_dict[tuple(plant.position + trial_direction)]
                    if plant.can_overshadow(defending_plant):
                        w.kill(defending_plant)
                        w.spawn(plant.reproduce(trial_direction))
                        plant_index = alive_plants.index(plant) + 1
                        continue
                except KeyError:
                    pass
        plant_index += 1

    # Bug life cycle
    bug_index = 0
    while bug_index < len(alive_bugs):
        bug = alive_bugs[bug_index]

        # Should it die?
        if bug.energy <= 0:
            w.kill(bug)
            continue

        bug.respire()

        # Try move (if not newly born)
        if bug.lifetime > 1 or w.time == 1:
            trial_direction = Direction.random()

            if w.available(bug, trial_direction):
                w.grid[tuple(bug.position)] -= bug.value
                bug.move(trial_direction)
                w.grid[tuple(bug.position)] += bug.value

        # Can it eat?
        if w.grid[tuple(bug.position)] == FOOD_VAL + BUG_VAL:
            plant_beneath = w.plant_position_dict[tuple(bug.position)]
            if bug.try_eat(plant_beneath):
                w.kill(plant_beneath)

        # Can it reproduce?
        if bug.energy >= bug.reproduction_threshold and bug.lifetime > 1:
            trial_direction = Direction.random()
            if w.available(bug, trial_direction):
                w.spawn(bug.reproduce(trial_direction))

        bug_index += 1

########################
# --------Plot-------- #
########################
world_recorder.output_world_stats()
world_recorder.output_world_data()
world_viewer.plot_world_stats()
world_viewer.plot_world_data()
