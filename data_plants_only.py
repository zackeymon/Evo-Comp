import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from data_analysis import objective, restricted_growth, CC

data = np.loadtxt('plant_only.csv')
t = np.arange(0, len(data), 1)

guess = np.array([0.01])
bounds = ((0, 0.5),)

opt = minimize(objective, guess, args=(restricted_growth, data), bounds=bounds)
print(opt)
sol = odeint(restricted_growth, data[0], t, args=tuple(opt.x))

plt.plot(t, data/CC, '-', label='Simulated Data')
plt.plot(t, sol/CC, '-', label='L-V Model')
plt.title('Plant population density, growth rate = 10')
plt.ylabel('Population Density')
plt.xlabel('Time')
plt.legend()
plt.show()
