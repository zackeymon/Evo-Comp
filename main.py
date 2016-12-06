import _thread
import random
import evolution_switches as es
from world import World
from direction import Direction
from organism_type import OrganismType
from world_recorder import WorldRecorder
from world_viewer import WorldViewer

# #######Initialisation####### #
my_world = World(rows=80, columns=80, fertile_lands=[[[10, 10], [69, 69]]])
# my_world = World(rows=3, columns=3)

world_viewer = WorldViewer(my_world)
gene_viewer = GeneViewer(my_world)

my_world.spawn_food(200)
my_world.spawn_bug(50)


# Kill switch
def input_thread(list_):
    input()
    list_.append(None)


_list = []
_thread.start_new_thread(input_thread, (_list,))

# #######Run####### #
while len(my_world.bug_list) > 0 and not _list:

    # generate data
    world_recorder.generate_world_stats()
    world_recorder.generate_world_data()
    world_viewer.view_world(my_world)

    # spawn food
    my_world.available_spaces()
    my_world.spawn_food(1, taste=0.0 + my_world.food_taste_average)

    random.shuffle(my_world.food_list)
    random.shuffle(my_world.bug_list)

    # food life cycle
    for food in my_world.food_list:
        if food.lifetime > 0 or my_world.time == 0:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # Find an empty square
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    new_food = food.reproduce(random_direction)
                    my_world.food_list.append(new_food)
                    my_world.grid[tuple(new_food.position)] += OrganismType.food
        food.lifetime += 1

    # bug life cycle
    i = 0
    my_world.dead_food_list.append([])
    my_world.dead_bug_list.append([])
    while i < len(my_world.bug_list):
        bug = my_world.bug_list[i]
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            my_world.kill(bug)
        else:
            # Bug won't move if born this turn
            if bug.lifetime > 0 or my_world.time == 0:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    my_world.grid[tuple(bug.position)] -= OrganismType.bug
                    bug.move(random_direction)
                    my_world.grid[tuple(bug.position)] += OrganismType.bug

            # Check if bug can eat food
            for j, food in enumerate(my_world.food_list):
                if (bug.position == food.position).all():
                    if bug.taste - 10 <= food.taste <= bug.taste + 10:
                        bug.eat(food)
                        my_world.kill(food)
                    break

            # Check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    new_bug = bug.reproduce(random_direction)
                    my_world.bug_list.append(new_bug)
                    my_world.grid[tuple(new_bug.position)] += OrganismType.bug
            bug.lifetime += 1
            i += 1

    print("time: %i" % my_world.time)
    my_world.time += 1

# #######Plot####### #
world_recorder.output_world_stats()
world_recorder.output_world_data()
world_viewer.plot_world_stats()
world_viewer.plot_world_data(world=True, genes=True)
