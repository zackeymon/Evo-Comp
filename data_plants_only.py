import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from data_analysis import objective, restricted_growth

data = np.loadtxt('plant_rt30_gr2.csv')
t = np.arange(0, len(data), 1)

guess = [0.01]
bounds = ((0, 0.5),)

# 2D minimisation??

opt = minimize(objective, guess, args=(restricted_growth, data), bounds=bounds)
print(opt)
sol = odeint(restricted_growth, data[0], t, args=tuple(opt.x))

plt.plot(t, data/40000, '.-', label='Plant Population')
plt.plot(t, sol/40000, '.-', label='L-V Model')
plt.show()
