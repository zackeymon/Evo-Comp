import _thread
import random
import config as cfg
from utility_methods import *
from direction import Direction
from organism_type import OrganismType
from world import World
from world_recorder import WorldRecorder
from world_viewer import WorldViewer

# #######Initialisation####### #
my_world = World(**cfg.world['settings'])

world_recorder = WorldRecorder(my_world)
world_viewer = WorldViewer(my_world.seed)

my_world.spawn_food(int(len(my_world.fertile_squares) / 20), **cfg.world['spawn_values']['food'])
my_world.spawn_bug(int(len(my_world.fertile_squares) / 40), **cfg.world['spawn_values']['bug'])


# Kill switch
def input_thread(list_):
    input()
    list_.append(None)


_list = []
_thread.start_new_thread(input_thread, (_list,))

# #######Run####### #
while len(my_world.organism_lists['bug']['alive']) > 0 and not _list:

    # generate data
    world_recorder.generate_world_stats()
    world_recorder.generate_world_data()
    world_viewer.view_world(my_world)

    # spawn food
    my_world.available_spaces()
    my_world.spawn_food(1, **cfg.world['spawn_values']['food'], taste=my_world.food_taste_average)

    random.shuffle(my_world.organism_lists['food']['alive'])
    random.shuffle(my_world.organism_lists['bug']['alive'])

    # food life cycle
    for food in my_world.organism_lists['food']['alive']:
        if food.lifetime > 0 or my_world.time == 0:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # find an empty square
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    new_food = food.reproduce(random_direction)
                    my_world.organism_lists['food']['alive'].append(new_food)
                    my_world.grid[tuple(new_food.position)] += OrganismType.food
        food.lifetime += 1

    # bug life cycle
    i = 0
    my_world.organism_lists['food']['dead'].append([])
    my_world.organism_lists['bug']['dead'].append([])
    while i < len(my_world.organism_lists['bug']['alive']):
        bug = my_world.organism_lists['bug']['alive'][i]
        bug.respire()
        if bug.energy <= 0:
            # bug die
            my_world.kill(bug)
        else:
            # bug won't move if born this turn
            if bug.lifetime > 0 or my_world.time == 0:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    my_world.grid[tuple(bug.position)] -= OrganismType.bug
                    bug.move(random_direction)
                    my_world.grid[tuple(bug.position)] += OrganismType.bug

            # check if there is food on this square
            if my_world.grid[tuple(bug.position)] == OrganismType.food_bug:
                for j, food in enumerate(my_world.organism_lists['food']['alive']):
                    # find the food
                    if (bug.position == food.position).all():
                        # check if bug can eat it
                        if np.absolute(bug.taste - get_taste_average([bug.taste, food.taste])) < 10:
                            bug.eat(food)
                            my_world.kill(food)
                        break

            # check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold and bug.lifetime > 0:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                # check if there is an empty square
                if random_direction is not None:
                    new_bug = bug.reproduce(random_direction)
                    my_world.organism_lists['bug']['alive'].append(new_bug)
                    my_world.grid[tuple(new_bug.position)] += OrganismType.bug
            bug.lifetime += 1
            i += 1

    print("time: %i" % my_world.time)
    my_world.time += 1

# #######Plot####### #
world_recorder.output_world_stats()
world_recorder.output_world_data()
world_viewer.plot_world_stats()
world_viewer.plot_world_data()
