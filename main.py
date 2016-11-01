import random
from world import World
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer


world1 = World(rows=20, columns=20)
world_viewer1 = WorldViewer()

world1.initialise_food(200, energy=25, reproduction_threshold=30, energy_max=100)
world1.initialise_bug(10, energy=5, reproduction_threshold=70, energy_max=100)


for i in range(10):
#while world1.bugList:
#    if (world1.time % 2 == 0):
#        world1.foodList.append(Food(World.random_position(world1)))

    print(world1.bugList)
    world_viewer1.view_world(world1)
    world_viewer1.output_data_population(world1)

    random.shuffle(world1.bugList)
    random.shuffle(world1.foodList)

    for food in world1.foodList:
        if world1.time == 0 or food.lifetime >= 1:
            food.grow()
            if food.energy >= food.reproduction_threshold:
                # Find an empty square
                random_direction = Direction.random(
                    world1.get_disallowed_directions(food.position, OrganismType.food))
                if random_direction is not None:
                    world1.foodList.append(food.reproduce(random_direction))
        food.lifetime += 1

    for bug in world1.bugList:
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            world1.bugList.remove(bug)
            world1.bugList_dead.append(bug)
        else:
            if world1.time == 0 or bug.lifetime >= 1:
                random_direction = Direction.random(
                    world1.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    bug.move(random_direction)
            # for i in world1.grid[bug.position[0]][bug.position[1]]:
            #     if isinstance(i, Food):
            #         bug.eat(i)

            for food in world1.foodList:
                if (bug.position == food.position).all():
                    bug.eat(food)
                    world1.foodList.remove(food)
                    world1.foodList_dead.append(food)
                    break

            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    world1.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    world1.bugList.append(bug.reproduce(random_direction))

        bug.lifetime += 1

    world1.time += 1

