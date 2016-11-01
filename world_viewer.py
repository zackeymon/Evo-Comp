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

        if not os.path.exists(os.path.join('data', self.time_stamp)):
            os.makedirs(os.path.join('data', self.time_stamp))

        plt.savefig(os.path.join('data', self.time_stamp, '%s.png' % world.time))
        plt.close()

    def output_data_population(self, world):
        """Output data for analysis."""

        if world.time == 0:
            with open(os.path.join('data', self.time_stamp, 'food_population.txt'), 'a') as food_file:
                food_file.write('time' + '   ' + 'population' + '\n')
            with open(os.path.join('data', self.time_stamp, 'bug_population.txt'), 'a') as bug_file:
                bug_file.write('time' + '   ' + 'population' + '\n')
            with open(os.path.join('data', self.time_stamp, 'food_alive_lifetime.txt'), 'a') as food_life_alive:
                food_life_alive.write('time' + '   ' + 'average_alive_lifetime' + '\n')
            with open(os.path.join('data', self.time_stamp, 'bug_alive_lifetime.txt'), 'a') as bug_life_alive:
                bug_life_alive.write('time' + '   ' + 'average_alive_lifetime' + '\n')
            with open(os.path.join('data', self.time_stamp, 'food_lifetime.txt'), 'a') as food_life_dead:
                food_life_dead.write('time' + '   ' + 'average_lifetime' + '\n')
            with open(os.path.join('data', self.time_stamp, 'bug_lifetime.txt'), 'a') as bug_life_dead:
                bug_life_dead.write('time' + '   ' + 'average_lifetime' + '\n')

        with open(os.path.join('data', self.time_stamp, 'food_population.txt'), 'a') as food_file:
            food_file.write('%s' % world.time + '      ' + '%r' % np.size(world.foodList) + '\n')

        with open(os.path.join('data', self.time_stamp, 'bug_population.txt'), 'a') as bug_file:
            bug_file.write('%s' % world.time + '      ' + '%r' % np.size(world.bugList) + '\n')

        with open(os.path.join('data', self.time_stamp, 'food_alive_lifetime.txt'), 'a') as food_life_alive:
            food_life_alive.write('%s' % world.time + '      ' + '%r' % (self.sum_list_lifetime(world.foodList) / np.size(world.foodList)) + '\n')

        with open(os.path.join('data', self.time_stamp, 'bug_alive_lifetime.txt'), 'a') as bug_life_alive:
            bug_life_alive.write('%s' % world.time + '      ' + '%r' % (self.sum_list_lifetime(world.bugList) / np.size(world.bugList)) + '\n')

        if np.size(world.foodList_dead) > 0:
            with open(os.path.join('data', self.time_stamp, 'food_lifetime.txt'), 'a') as food_life_dead:
                food_life_dead.write('%s' % world.time + '      ' + '%r' % (self.sum_list_lifetime(world.foodList_dead) / np.size(world.foodList_dead)) + '\n')

        if np.size(world.bugList_dead) > 0:
            with open(os.path.join('data', self.time_stamp, 'bug_lifetime.txt'), 'a') as bug_life_dead:
                bug_life_dead.write('%s' % world.time + '      ' + '%r' % (self.sum_list_lifetime(world.bugList_dead) / np.size(world.bugList_dead)) + '\n')
