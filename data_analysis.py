import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize


def lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    # if x < 5: x = 5
    # if y < 5: y = 5
    dx_dt = alpha * x - beta * x * y
    dy_dt = delta * x * y - gamma * y
    return [dx_dt, dy_dt]


def objective(parameters, data):
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    lv_model = odeint(lv, data[0], t, args=tuple(parameters))
    return np.sum(np.abs(data - lv_model)) / sample_size


if __name__ == '__main__':
    guess_parameters = [0.1, 0.001, 0.001, 0.5]
    parameters_bounds = ((0, None), (0, None), (0, None), (0, None))
    # TODO: Constraint dictionary

    data = np.loadtxt('population_data.csv', delimiter=',')
    t = np.arange(0, len(data), 1)

    plt.plot(t, data[:, 0], t, data[:, 1])

    opt_parameters = minimize(objective, guess_parameters, args=(data,), tol=0.001, bounds=parameters_bounds)
    print(opt_parameters.x)

    sol = odeint(lv, data[0], t, args=tuple(opt_parameters.x))
    plt.plot(t, sol[:, 0], t, sol[:, 1])

    plt.show()
