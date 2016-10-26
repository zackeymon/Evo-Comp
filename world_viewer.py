# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:29:07 2016

@author: acl114
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse
from world import World

class WorldViewer:
    
    def view_world(self, world):
        ax = plt.figure(figsize=(self.columns, self.rows)).add_subplot(1,1,1)  

        for food in world.FoodList:
            food_size = food.energy*0.01
            ax.add_patch(Rectangle((food.position[0]+(0.5-food_size/2), food.position[1]+(0.5-food_size/2)), food_size, food_size, facecolor = "#228b22"))
                
        for bug in world.BugList:
            bug_size = bug.energy*0.01
            if bug_size <= 0.3:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=0.3, height=0.3, facecolor = "#7b68ee"))
            else:
                ax.add_patch(Ellipse(xy=(bug.position[0]+0.5, bug.position[1]+0.5), width=bug_size, height=bug_size, facecolor = "#7b68ee"))
            
        ax.set_xticks(np.arange(0, self.columns+2, 1))                                                                                              
        ax.set_yticks(np.arange(0, self.rows+2, 1))  
        
        ax.savefig('/data/' + str(world) + '/' + str(world.time) + '.png')
        plt.close(ax)


#fig.savefig('Pics2/forcing' + str(forcing) + 'damping' + str(damping) + 'omega' + str(omega) + 'set2.png')

#fig.savefig(os.path.join(('Pics2', 'forcing{0}damping{1}omega{2}set2.png'.format(forcing, damping, omega)))

#path = '/Some/path/to/Pics2'
#filename = 'forcing{0}damping{1}omega{2}set2.png'.format(forcing, damping, omega)
#filename = os.path.join(path, filename)
#fig.savefig(filename)