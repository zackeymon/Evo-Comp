import random
from world import World
from food import Food
from bug import Bug
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer
from gene_viewer import GeneViewer

myWorld = World(rows=30, columns=30)
worldViewer = WorldViewer()
geneViewer = GeneViewer()
random.seed(worldViewer.time_stamp)

worldSpaces= myWorld.grid
myWorld.spawn_food(100)
myWorld.spawn_bug(10)

worldViewer.world_seed(myWorld)  #seed information irrelevant until we start collecting data properly, can put bad results in here so we don't need to keep them but can check them later

for i in range(2):

    if len(myWorld.bugList) == 0:
        break

    myWorld.available_spaces()
    myWorld.spawn_food(1)

    random.shuffle(myWorld.bugList)
    random.shuffle(myWorld.foodList)

    for food in myWorld.foodList:
        if food.lifetime > 0:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # Find an empty square
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    myWorld.foodList.append(food.reproduce(random_direction))
        food.lifetime += 1
    
    for bug in list(myWorld.bugList):
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            myWorld.bugList.remove(bug)
            myWorld.bugListDead.append(bug)
        else:
            if bug.lifetime > 0:
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction:
                    bug.move(random_direction)

            # for i in myWorld.grid[bug.position[0]][bug.position[1]]:
            #     if isinstance(i, Food):
            #         bug.eat(i)

            for food in myWorld.foodList:
                if (bug.position == food.position).all():
                    bug.eat(food)
                    myWorld.foodList.remove(food)
                    myWorld.foodListDead.append(food)
                    break

            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction:
                    myWorld.bugList.append(bug.reproduce(random_direction))
            bug.lifetime += 1

    worldViewer.generate_data(myWorld)
    geneViewer.generate_gene_data(myWorld)
    worldViewer.view_world(myWorld)
    myWorld.time += 1

worldViewer.output_data(myWorld)
geneViewer.output_gene_data(myWorld)
geneViewer.plot_gene_data(myWorld)
