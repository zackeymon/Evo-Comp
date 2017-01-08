from data_analysis import competitive_lv, objective, lv
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution

t = np.arange(0, 140, 1)
init_populations = [10, 10]

parameters = [0.1, 0.02, 0.02, 0.4]

sol = odeint(lv, init_populations, t, args=tuple(parameters))

guess = [0.2, 0.03, 0.04, 0.3]
bounds = ((0, None), (0, None), (0, None), (0, None))

opt_parameters = minimize(objective, guess, args=(sol,), bounds=bounds)
print(opt_parameters.x)
