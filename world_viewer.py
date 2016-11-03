import numpy as np
import os
import datetime
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse


class WorldViewer:
    """
    A class to view the world visually as it develops.
    """
    def __init__(self, time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')):
        """
        World Initialisation Time
        :param time_stamp: The beginning of time
        """
        self.time_stamp = time_stamp

        if not os.path.exists(os.path.join('data', self.time_stamp)):
            os.makedirs(os.path.join('data', self.time_stamp))

    def sum_list_lifetime(self, object_list):
        lifetime = 0
        for object in object_list:
            lifetime += object.lifetime
        return lifetime

    def view_world(self, world):
        """"Draw the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(world.columns, world.rows)).add_subplot(1,1,1)

        for food in world.foodList:
            food_size = food.energy*0.01
            if food_size <= 0.3:
                ax.add_patch(Rectangle((food.position[0]+(0.5-0.3/2), food.position[1]+(0.5-0.3/2)), 0.3, 0.3, facecolor = "#228b22"))
            else:
                ax.add_patch(Rectangle((food.position[0]+(0.5-food_size/2), food.position[1]+(0.5-food_size/2)), food_size, food_size, facecolor = "#228b22"))
                
        for bug in world.bugList:
            bug_size = bug.energy*0.01
            if bug_size <= 0.3:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=0.3, height=0.3, facecolor = "#ff0000"))
            else:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=bug_size, height=bug_size, facecolor = "#ff0000"))
            
        ax.set_xticks(np.arange(0, world.columns+1, 1))
        ax.set_yticks(np.arange(0, world.rows+1, 1))
        plt.xlabel('time=%s' %world.time, fontsize=(2*world.columns))
        #ax.grid(b=True, which='major', color='black', linestyle='-')

        plt.savefig(os.path.join('data', self.time_stamp, '%s.png' % world.time))
        plt.close()

    def generate_data(self, world):
        """Add data for the current world iteration to a list."""

        world.food_data[0].append(world.time)
        world.food_data[1].append(len(world.foodList))
        world.food_data[2].append(len(world.foodListDead))
        if len(world.foodList) <= 0:
            world.food_data[3].append('0')
        else:
            world.food_data[3].append(self.sum_list_lifetime(world.foodList) / len(world.foodList))
        if len(world.foodListDead) <=0:
            world.food_data[4].append('N/A')
        else:
            world.food_data[4].append(self.sum_list_lifetime(world.foodListDead) / len(world.foodListDead))

        world.bug_data[0].append(world.time)
        world.bug_data[1].append(len(world.bugList))
        world.bug_data[2].append(len(world.bugListDead))
        if len(world.bugList) <= 0:
            world.bug_data[3].append('0')
        else:
            world.bug_data[3].append(self.sum_list_lifetime(world.bugList) / len(world.bugList))
        if len(world.bugListDead) <=0:
            world.bug_data[4].append('N/A')
        else:
            world.bug_data[4].append(self.sum_list_lifetime(world.bugListDead) / len(world.bugListDead))

    def output_data(self, world):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.time_stamp, 'food_data.csv'), 'a') as food_file:
            for time, population, dead_population, average_alive_lifetime, average_lifespan in zip(*world.food_data):
                food_file.write('%r,' % time + '%r,' % population + '%r,' % dead_population + '%r,' % average_alive_lifetime + '%r,' % average_lifespan + '\n')

        with open(os.path.join('data', self.time_stamp, 'bug_data.csv'), 'a') as bug_file:
            for time, population, dead_population, average_alive_lifetime, average_lifespan in zip(*world.bug_data):
                bug_file.write('%r,' % time + '%r,' % population + '%r,' % dead_population + '%r,' % average_alive_lifetime + '%r,' % average_lifespan + '\n')

