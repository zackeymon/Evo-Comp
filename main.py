import _thread
import random
import evolution_switches as es
from world import World
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer
from gene_viewer import GeneViewer

# #######Initialisation####### #
my_world = World(rows=30, columns=30)
world_viewer = WorldViewer(my_world)
gene_viewer = GeneViewer(my_world)
random.seed(my_world.seed)

my_world.spawn_food(100)
my_world.spawn_bug(20)


# Kill switch
def input_thread(list_):
    input()
    list_.append(None)


_list = []
_thread.start_new_thread(input_thread, (_list,))

# #######Run####### #
while len(my_world.bug_list) > 0 and not _list:

    world_viewer.view_world_data()
    world_viewer.generate_data()
    gene_viewer.generate_gene_data()
    world_viewer.view_world()

    my_world.available_spaces()
    my_world.spawn_food(1, gene_val=0.0 + gene_viewer.food_gene_average)

    random.shuffle(my_world.food_list)
    random.shuffle(my_world.bug_list)

    for food in my_world.food_list:
        if food.lifetime > 0:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # Find an empty square
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    my_world.food_list.append(food.reproduce(random_direction))
        food.lifetime += 1

    i = 0
    my_world.dead_food_list.append([])
    my_world.dead_bug_list.append([])
    while i < len(my_world.bug_list):
        bug = my_world.bug_list[i]
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            my_world.dead_bug_list[-1].append(my_world.bug_list.pop(i))
        else:
            # Bug won't move if born this turn
            if bug.lifetime > 0:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    bug.move(random_direction)

            # for i in myWorld.grid[bug.position[0]][bug.position[1]]:
            #     if isinstance(i, Food):
            #         bug.eat(i)

            # Check if bug can eat food
            for j, food in enumerate(my_world.food_list):
                if (bug.position == food.position).all():
                    if bug.gene_val-10 < food.gene_val < bug.gene_val+10:
                        bug.eat(food)
                        my_world.dead_food_list[-1].append(my_world.food_list.pop(j))
                    break

            # Check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    my_world.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    spawn = bug.reproduce(random_direction)
                    my_world.bug_list.append(spawn)
            bug.lifetime += 1
            i += 1

    print("time: %i" % my_world.time)
    my_world.time += 1

# #######Plot####### #
world_viewer.output_data()
world_viewer.plot_data()
gene_viewer.output_gene_data()
gene_viewer.plot_gene_data()
world_viewer.output_world_data()
# worldViewer.plot_world_data()
