import _thread
import random
import config as cfg
from utility_methods import *
from direction import Direction
from constants import *
from world import World
from world_recorder import WorldRecorder
from world_viewer import WorldViewer


# #######Initialisation####### #
# Make a kill switch
def input_thread(list_):
    input()
    list_.append(None)


_list = []
_thread.start_new_thread(input_thread, (_list,))

my_world = World(**cfg.world['settings'])

world_recorder = WorldRecorder(my_world)
world_viewer = WorldViewer(my_world.seed)

# Populate the world
my_world.drop_food(int(len(my_world.fertile_squares) / 20), **cfg.world['food_spawn_vals'])
my_world.drop_bug(int(len(my_world.fertile_squares) / 40), **cfg.world['bug_spawn_vals'])

# #######Run####### #
while len(my_world.organism_lists[BUG_NAME]['alive']) > 0 and not _list:
    # generate yesterday data
    world_recorder.generate_world_stats()
    world_recorder.generate_world_data()
    world_viewer.view_world(my_world)

    my_world.prepare_today()

    # food life cycle
    for food in my_world.organism_lists[FOOD_NAME]['alive']:
        food.grow()
        if food.energy >= food.reproduction_threshold:
            # find an empty square
            random_direction = Direction.random(
                my_world.get_disallowed_directions(food.position, FOOD_VAL))
            if random_direction is not None:
                new_food = food.reproduce(random_direction)
                my_world.organism_lists[FOOD_NAME]['alive'].append(new_food)
                my_world.grid[tuple(new_food.position)] += FOOD_VAL

    # bug life cycle
    bug_index = 0
    while bug_index < len(my_world.organism_lists[BUG_NAME]['alive']):
        bug = my_world.organism_lists[BUG_NAME]['alive'][bug_index]
        bug.respire()
        if bug.energy <= 0:
            # bug die
            my_world.kill(bug)
        else:
            # bug won't move if born this turn
            if bug.lifetime > 1 or my_world.time == 1:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, BUG_VAL))
                if random_direction is not None:
                    my_world.grid[tuple(bug.position)] -= BUG_VAL
                    bug.move(random_direction)
                    my_world.grid[tuple(bug.position)] += BUG_VAL

            # check if there is food on this square
            if my_world.grid[tuple(bug.position)] == FOOD_VAL + BUG_VAL:
                for j, food in enumerate(my_world.organism_lists[FOOD_NAME]['alive']):
                    # find the food
                    if (bug.position == food.position).all():
                        # check if bug can eat it
                        if np.absolute(bug.taste - get_taste_average([bug.taste, food.taste])) <= 10:
                            bug.eat(food)
                            my_world.kill(food)
                        break

            # check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold and bug.lifetime > 0:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, BUG_VAL))
                # check if there is an empty square
                if random_direction is not None:
                    new_bug = bug.reproduce(random_direction)
                    my_world.organism_lists[BUG_NAME]['alive'].append(new_bug)
                    my_world.grid[tuple(new_bug.position)] += BUG_VAL
            bug_index += 1

# #######Plot####### #
world_recorder.output_world_stats()
world_recorder.output_world_data()
world_viewer.plot_world_stats()
world_viewer.plot_world_data()
