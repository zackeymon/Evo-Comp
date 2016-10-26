import random
from world import World
from bug import Bug
from food import Food
from direction import Direction
from organism_type import OrganismType
from world_viewer import WorldViewer


def random_position(world):
    x = random.randint(0, world.columns - 1)
    y = random.randint(0, world.rows - 1)
    return [x, y]


world_viewer1 = WorldViewer()
world1 = World()

for i in range(2):
    world1.bugList.append(Bug(random_position(world1)))
    world1.foodList.append(Food(random_position(world1), energy=65))
    world1.foodList.append(Food(random_position(world1), energy=65))

for i in range(100):
    random.shuffle(world1.bugList)
    random.shuffle(world1.foodList)
    for food in world1.foodList:
        food.grow()
        if food.energy >= food.reproduction_threshold:
            # Find an empty square
            random_direction = Direction.random(
                world1.get_disallowed_directions(food.position, OrganismType.food))
            if random_direction is not None:
                world1.foodList.append(food.reproduce(random_direction))

    for bug in world1.bugList:
        bug.respire()
        if bug.energy <= 0:
            # Bug die
            world1.bugList.remove(bug)
        else:
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
                    break

            if bug.energy >= bug.reproduction_threshold:
                random_direction = Direction.random(
                    world1.get_disallowed_directions(bug.position, OrganismType.bug))
                if random_direction is not None:
                    world1.bugList.append(bug.reproduce(random_direction))

    world_viewer1.view_world(world1)
    print(world1.bugList)
