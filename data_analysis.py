import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize


def lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    dx_dt = alpha * x - beta * x * y
    dy_dt = delta * x * y - gamma * y
    return [dx_dt, dy_dt]


def objective(parameters, data):
    t = np.arange(0, len(data), 1)
    model = odeint(lv, data[0], t, args=parameters)
    return np.sum((data - model) ** 2) / len(data)


guess_parameters = [0.8, 0.001, 0.001, 0.2]

# plt.plot(t, sol[:, 0], t, sol[:, 1])

plt.show()
