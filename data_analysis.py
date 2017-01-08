import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution


def lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    # print(population)
    dx_dt = x * (alpha - beta * y)
    dy_dt = y * (delta * x - gamma)
    return [dx_dt, dy_dt]


def competitive_lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    carrying_capacity = 2500
    dx_dt = alpha * x * (1 - x / carrying_capacity) - beta * x * y
    dy_dt = delta * x * y - gamma * y * (1 - y / carrying_capacity)
    return [dx_dt, dy_dt]


# TODO: Competitive LV
# I think the objective function is right. We need better data sets

def objective(parameters, data):
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    lv_model = odeint(competitive_lv, data[0], t, args=tuple(parameters))
    return np.sum(np.abs(lv_model - data))


if __name__ == '__main__':
    guess_parameters = [0.08, 0.0002, 0.001, 0.01]
    parameters_bounds = ((0.0000001, 0.2), (0.0000001, 0.2), (0.0000001, 0.2), (0.0000001, 0.2))
    # TODO: Constraint dictionary

    data = np.loadtxt('population_data.csv', delimiter=',')
    t = np.arange(0, len(data), 1)

    plt.plot(t, data[:, 0], t, data[:, 1])
    opt_parameters = differential_evolution(objective, parameters_bounds, args=(data,))
    # opt_parameters = minimize(objective, guess_parameters, args=(data,), bounds=parameters_bounds)
    print(opt_parameters)

    sol = odeint(competitive_lv, data[0], t, args=tuple(opt_parameters.x))
    plt.plot(t, sol[:, 0], 'black')
    plt.plot(t, sol[:, 1], 'red')
    plt.show()
