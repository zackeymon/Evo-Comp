import thread
import random
import evolution_switches as es
from world import World
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer
from gene_viewer import GeneViewer

# #######Initialisation####### #
myWorld = World(rows=30, columns=30)
worldViewer = WorldViewer(myWorld)
geneViewer = GeneViewer(myWorld)
random.seed(myWorld.seed)

myWorld.spawn_food(100)
myWorld.spawn_bug(20)


# Kill switch
def input_thread(list_):
    raw_input()
    list_.append(None)


_list = []
thread.start_new_thread(input_thread, (_list,))

# #######Run####### #
while len(myWorld.bug_list) > 0 and not _list:

    worldViewer.view_world_data()
    worldViewer.generate_data()
    geneViewer.generate_gene_data()
    worldViewer.view_world()

    myWorld.available_spaces()
    myWorld.spawn_food(1, gene_val=0.0 + geneViewer.food_gene_average)

    random.shuffle(myWorld.food_list)
    random.shuffle(myWorld.bug_list)

    for food in myWorld.food_list:
        if food.lifetime > 0:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # Find an empty square
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    myWorld.food_list.append(food.reproduce(random_direction))
        food.lifetime += 1

    i = 0
    myWorld.dead_food_list.append([])
    myWorld.dead_bug_list.append([])
    while i < len(myWorld.bug_list):
        bug = myWorld.bug_list[i]
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            myWorld.dead_bug_list[-1].append(myWorld.bug_list.pop(i))
        else:
            # Bug won't move if born this turn
            if bug.lifetime > 0:
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    bug.move(random_direction)

            # for i in myWorld.grid[bug.position[0]][bug.position[1]]:
            #     if isinstance(i, Food):
            #         bug.eat(i)

            # Check if bug can eat food
            for j, food in enumerate(myWorld.food_list):
                if (bug.position == food.position).all():
                    if bug.gene_val-10 < food.gene_val < bug.gene_val+10:
                        bug.eat(food)
                        myWorld.dead_food_list[-1].append(myWorld.food_list.pop(j))
                    break

            # Check if bug can reproduce
            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    spawn = bug.reproduce(random_direction)
                    myWorld.bug_list.append(spawn)
            bug.lifetime += 1
            i += 1

    print("time: %i" % myWorld.time)
    myWorld.time += 1

# #######Plot####### #
worldViewer.output_data()
worldViewer.plot_data()
geneViewer.output_gene_data()
geneViewer.plot_gene_data()
worldViewer.output_world_data()
# worldViewer.plot_world_data()
