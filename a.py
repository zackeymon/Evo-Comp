import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, RegularPolyCollection
import matplotlib as mpl

# Generate data. In this case, we'll make a bunch of center-points and generate
# verticies by subtracting random offsets from those center-points
numpoly, numverts = 100, 4
centers = 100 * (np.random.random((numpoly,2)) - 0.5)
offsets = 10 * (np.random.random((numverts,numpoly,2)) - 0.5)
verts = centers + offsets
verts = np.swapaxes(verts, 0, 1)

# In your case, "verts" might be something like:
# verts = zip(zip(lon1, lat1), zip(lon2, lat2), ...)
# If "data" in your case is a numpy array, there are cleaner ways to reorder
# things to suit.

# Color scalar...
# If you have rgb values in your "colorval" array, you could just pass them
# in as "facecolors=colorval" when you create the PolyCollection
z = np.random.random(numpoly) * 500

ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)

ax.set_xticks(np.arange(0, 10))
ax.set_yticks(np.arange(0, 10))
# Make the collection and add it to the plot.
food_collection = RegularPolyCollection(4, sizes=[100,100], offsets=[[5,5],[4,4]], transOffset=ax.transData, facecolors=['r', 'g'])
ax.add_collection(food_collection)
# coll = PolyCollection(verts, array=z, cmap=mpl.cm.jet, edgecolors='none')
# ax.add_collection(coll)

# Add a colorbar for the PolyCollection
# fig.colorbar(coll, ax=ax)
plt.show()

print(list(zip([1,1], [2,2])))
