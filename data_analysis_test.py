from data_analysis import competitive_lv, objective, lv
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution, basinhopping

t = np.arange(0, 100, 1)
init_populations = [100, 100]

parameters = [0.1, 0.002, 0.002, 0.4]

sol = odeint(lv, init_populations, t, args=tuple(parameters))

plt.plot(t, sol[:, 0], t, sol[:, 1])

guess = [0.12, 0.003, 0.003, 0.39]
bounds = ((1e-6, 1), (1e-6, 1), (1e-6, 1), (1e-6, 1))

opt_parameters = minimize(objective, guess, args=(sol,), bounds=bounds)
# opt_parameters = basinhopping(objective, guess, niter=1000, minimizer_kwargs={'args': (sol,)})

print(opt_parameters.x)

lv_model = odeint(lv, init_populations, t, args=tuple(opt_parameters.x))


plt.plot(t, lv_model[:, 0], t, lv_model[:, 1])

plt.show()