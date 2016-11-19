import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse


class WorldViewer:
    """
    A class to view the world visually as it develops.
    """
    def __init__(self, world):
        """
        World Viewer Initialisation
        :param world: The world being viewed
        """
        self.world = world

        if not os.path.exists(os.path.join('data', world.seed)):
            os.makedirs(os.path.join('data', world.seed))

        if not os.path.isfile(os.path.join('data', 'world_seeds.csv')):
            with open(os.path.join('data', 'world_seeds.csv'), 'a') as seed:
                seed.write('time_stamp,' + 'columns,' + 'rows,' + 'food,' + 'bugs,' + 'results,' + '\n')

        with open(os.path.join('data', 'world_seeds.csv'), 'a') as seed:
            seed.write('%r,' % world.seed + '%r,' % world.columns + '%r,' % world.rows + '%r,'
                       % len(world.food_list) + '%r,' % len(world.bug_list) + '\n')

    @staticmethod
    def sum_list_lifetime(object_list, living=False):
        lifetime = 0

        if living is False:
            for i in object_list:
                for thing in i:
                    lifetime += thing.lifetime

            return lifetime

        else:
            for thing in object_list:
                lifetime += thing.lifetime

            return lifetime

    def view_world(self):
        """"Draw the world: rectangles=food, circles=bugs"""
        ax = plt.figure(figsize=(self.world.columns, self.world.rows)).add_subplot(1, 1, 1)

        for food in self.world.food_list:
            food_size = food.energy*0.01
            if food_size <= 0.3:
                ax.add_patch(Rectangle((food.position[0]+(0.5-0.3/2), food.position[1]+(0.5-0.3/2)), 0.3, 0.3,
                                       facecolor="#228b22"))
            else:
                ax.add_patch(Rectangle((food.position[0]+(0.5-food_size/2), food.position[1]+(0.5-food_size/2)),
                                       food_size, food_size, facecolor="#228b22"))
                
        for bug in self.world.bug_list:
            bug_size = bug.energy*0.01
            if bug_size <= 0.3:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=0.3, height=0.3,
                                     facecolor="#ff0000"))
            else:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=bug_size, height=bug_size,
                                     facecolor="#ff0000"))
            
        ax.set_xticks(np.arange(0, self.world.columns+1, 1))
        ax.set_yticks(np.arange(0, self.world.rows+1, 1))
        plt.title('time=%s' % self.world.time, fontsize=(2*self.world.columns))
#       ax.grid(b=True, which='major', color='black', linestyle='-')

        plt.savefig(os.path.join('data', self.world.seed, '%s.png' % self.world.time))
        plt.close()

    def generate_data(self):
        """Add data for the current world iteration to a list."""
        if self.world.time > 10:
            del self.world.dead_food_list[0]
            del self.world.dead_bug_list[0]

        self.world.food_data['time'].append(self.world.time)
        self.world.food_data['population'].append(len(self.world.food_list))
        self.world.food_data['deaths'].append(sum([len(i) for i in self.world.dead_food_list]))
        if len(self.world.food_list) <= 0:
            self.world.food_data['average_alive_lifetime'].append(0)
        else:
            self.world.food_data['average_alive_lifetime'].append(
                self.sum_list_lifetime(self.world.food_list, living=True) / len(self.world.food_list))
        if sum([len(i) for i in self.world.dead_food_list]) <= 0:
            self.world.food_data['average_lifespan'].append(0)
        else:
            self.world.food_data['average_lifespan'].append(
                self.sum_list_lifetime(self.world.dead_food_list) / sum([len(i) for i in self.world.dead_food_list]))

        self.world.bug_data['time'].append(self.world.time)
        self.world.bug_data['population'].append(len(self.world.bug_list))
        self.world.bug_data['deaths'].append(sum([len(i) for i in self.world.dead_bug_list]))
        if len(self.world.bug_list) <= 0:
            self.world.bug_data['average_alive_lifetime'].append(0)
        else:
            self.world.bug_data['average_alive_lifetime'].append(
                self.sum_list_lifetime(self.world.bug_list, living=True) / len(self.world.bug_list))
        if sum([len(i) for i in self.world.dead_bug_list]) <= 0:
            self.world.bug_data['average_lifespan'].append(0)
        else:
            self.world.bug_data['average_lifespan'].append(
                self.sum_list_lifetime(self.world.dead_bug_list) / sum([len(i) for i in self.world.dead_bug_list]))

    def output_data(self):
        """Output data in CSV (comma-separated values) format for analysis."""

        with open(os.path.join('data', self.world.seed, 'food_data.csv'), 'a') as food_file:
            for time, population, dead_population, average_alive_lifetime, average_lifespan \
                    in zip(*self.world.food_data.values()):
                food_file.write('%r,' % time + '%r,' % population + '%r,' % dead_population + '%r,'
                                % average_alive_lifetime + '%r,' % average_lifespan + '\n')

        with open(os.path.join('data', self.world.seed, 'bug_data.csv'), 'a') as bug_file:
            for time, population, dead_population, average_alive_lifetime, average_lifespan \
                    in zip(*self.world.bug_data.values()):
                bug_file.write('%r,' % time + '%r,' % population + '%r,' % dead_population + '%r,'
                               % average_alive_lifetime + '%r,' % average_lifespan + '\n')

    def plot_data(self):
        """Read the CSV (comma-separated values) output and plot trends."""

        food_data = np.genfromtxt(os.path.join('data', self.world.seed, 'food_data.csv'), delimiter=',',
                                  names=['time', 'population', 'dead_population', 'average_alive_lifetime',
                                         'average_lifespan'])

        plt.plot(food_data['time'], food_data['population'], label='Alive')
        plt.plot(food_data['time'], food_data['dead_population'], label='Deaths')
        plt.xlabel('Time')
        plt.ylabel('Number of Food')
        plt.legend()
        plt.title('Food Populations')
        plt.savefig(os.path.join('data', self.world.seed, 'plot_food_population'))
        plt.close()

        plt.plot(food_data['time'], food_data['average_alive_lifetime'], label='Average Alive Lifetime')
        plt.plot(food_data['time'], food_data['average_lifespan'], label='Average Lifespan (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Lifetime')
        plt.legend()
        plt.title('Food Lifetimes')
        plt.savefig(os.path.join('data', self.world.seed, 'plot_food_lifetime'))
        plt.close()

        bug_data = np.genfromtxt(os.path.join('data', self.world.seed, 'bug_data.csv'), delimiter=',',
                                 names=['time', 'population', 'dead_population', 'average_alive_lifetime',
                                        'average_lifespan'])

        plt.plot(bug_data['time'], bug_data['population'], label='Alive')
        plt.plot(bug_data['time'], bug_data['dead_population'], label='Deaths')
        plt.xlabel('Time')
        plt.ylabel('Number of Bugs')
        plt.legend()
        plt.title('Bug Populations')
        plt.savefig(os.path.join('data', self.world.seed, 'plot_bug_population'))
        plt.close()

        plt.plot(bug_data['time'], bug_data['average_alive_lifetime'], label='Average Alive Lifetime')
        plt.plot(bug_data['time'], bug_data['average_lifespan'], label='Average Lifespan (last 10 cycles)')
        plt.xlabel('Time')
        plt.ylabel('Lifetime')
        plt.legend()
        plt.title('Bug Lifetimes')
        plt.savefig(os.path.join('data', self.world.seed, 'plot_bug_lifetime'))
        plt.close()
