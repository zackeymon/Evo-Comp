from data_analysis import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution, basinhopping

# Test data
alpha = 0.193485
gamma = 0.209544

t = np.arange(0, 100, 1)
init_populations = [100, 100]
parameters = [alpha, 0.002, 0.002, gamma]

sol = odeint(competitive_lv, init_populations, t, args=tuple(parameters))

plt.plot(t, sol[:, 0], t, sol[:, 1])

print(objective([0.002, 0.002], competitive_lv, alpha, gamma, sol))

# Minimise objective to obtain test parameters
bounds = ((1e-12, 1.0), (1e-12, 1.0))

opt = differential_evolution(objective, bounds, args=(competitive_lv, alpha, gamma, sol))
actual = [alpha, opt.x[0], opt.x[1], gamma]

# opt_parameters = minimize(objective, guess, args=(competitive_lv, sol), bounds=bounds)

print(opt)

lv_model = odeint(competitive_lv, init_populations, t, args=tuple(actual))
plt.plot(t, lv_model[:, 0], t, lv_model[:, 1])

plt.show()
