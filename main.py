import random
from world import World
from food import Food
from bug import Bug
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer

myWorld = World(rows=20, columns=20)
worldViewer = WorldViewer()

myWorld.initialise_food(200, energy=25, reproduction_threshold=30, energy_max=100)
myWorld.initialise_bug(10, energy=5, reproduction_threshold=70, energy_max=100)

for i in range(100):

    myWorld.foodList.append(Food(myWorld.random_position()))

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

    for bug in myWorld.bugList:
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            myWorld.bugList.remove(bug)
            myWorld.bugListDead.append(bug)
        else:
            if myWorld.time == 0 or bug.lifetime >= 1:
                random_direction = Direction.random(
                    myWorld.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
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
                if random_direction is not None:
                    myWorld.bugList.append(bug.reproduce(random_direction))
            bug.lifetime += 1

    worldViewer.view_world(myWorld)
    worldViewer.output_data_population(myWorld)
    myWorld.time += 1
