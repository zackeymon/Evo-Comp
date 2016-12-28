import config as cfg
from constants import *
from utility_methods import *
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
    # generate yesterday data
    world_recorder.generate_world_stats()
    world_recorder.generate_world_data()
    world_viewer.view_world(w)

    alive_plants, alive_bugs = w.prepare_today()

    # food life cycle
    plant_index = 0
    while plant_index < len(alive_plants):
        plant = alive_plants[plant_index]
        plant.grow()
        if plant.energy <= cfg.food['growth_rate']:
            # plant die
            w.kill(plant)
        else:
            if plant.energy >= plant.reproduction_threshold:
                # find an empty square
                random_direction = w.get_random_available_direction(plant)
                if random_direction is not None:
                    w.spawn(plant.reproduce(random_direction))
            plant_index += 1

    # bug life cycle
    bug_index = 0
    while bug_index < len(alive_bugs):
        bug = alive_bugs[bug_index]
        bug.respire()
        if bug.energy <= 0:
            # bug die
            w.kill(bug)
        else:
            # bug won't move if born this turn
            if bug.lifetime > 1 or w.time == 1:
                random_direction = w.get_random_available_direction(bug)
                if random_direction is not None:
                    w.grid[tuple(bug.position)] -= BUG_VAL
                    bug.move(random_direction)
                    w.grid[tuple(bug.position)] += BUG_VAL

            # check if there is food on this square
            if w.grid[tuple(bug.position)] == FOOD_VAL + BUG_VAL:
                for j, plant in enumerate(w.organism_lists[FOOD_NAME]['alive']):
                    # find the food
                    if (bug.position == plant.position).all():
                        # check if bug can eat it
                        if np.absolute(bug.taste - get_taste_average([bug.taste, plant.taste])) <= 10:
                            bug.eat(plant)
                            w.kill(plant)
                        break

            # check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold and bug.lifetime > 1:
                random_direction = w.get_random_available_direction(bug)
                # check if there is an empty square
                if random_direction is not None:
                    w.spawn(bug.reproduce(random_direction))

            bug_index += 1

########################
# --------Plot-------- #
########################
world_recorder.output_world_stats()
world_recorder.output_world_data()
world_viewer.plot_world_stats()
world_viewer.plot_world_data()
