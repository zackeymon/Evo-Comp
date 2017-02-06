import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize

CC = 128 * 128


def lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    dx_dt = x * (alpha - beta * y)
    dy_dt = y * (delta * x - gamma)
    return [dx_dt, dy_dt]


def competitive_lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    dx_dt = alpha * x * (1 - x / CC) - beta * x * y
    dy_dt = delta * x * y - gamma * y
    return [dx_dt, dy_dt]


def restricted_growth(x, t, alpha):
    dx_dt = alpha * x * (1 - x / CC)
    return dx_dt


def bug_death(y, t, gamma):
    dy_dt = -gamma * y
    return dy_dt


def objective(parameters, *args):
    func, data = args
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    model = np.array(odeint(func, data[0], t, args=tuple(parameters)))
    if model.shape[1] == 1:
        model = model.ravel()
    return np.sum(np.square(model - data)) / sample_size


def objective_2d(parameters, *args):
    func, alpha, gamma, data = args
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    model = np.array(odeint(func, data[0], t, args=tuple([alpha, parameters[0], parameters[1], gamma])))
    if model.shape[1] == 1:
        model = model.ravel()
    return np.sum(np.square(model - data)) / sample_size


if __name__ == '__main__':
    guess_parameters = [0.20705694, 5.02921384e-05, 6.85824820e-05, 0.209544]
    parameters_bounds = ((0.1, 0.3), (4e-05, 6e-05), (6e-05, 8e-05), (0.1, 0.3))

    data = np.loadtxt('para_fit_.csv', delimiter=',')  # [plants, bugs]
    t = np.arange(0, len(data), 1)

    plt.plot(t, data[:, 0], t, data[:, 1])
    opt_parameters = minimize(objective, guess_parameters, args=(competitive_lv, data), bounds=parameters_bounds)
    print(opt_parameters)

    sol = odeint(competitive_lv, data[0], t, args=tuple(opt_parameters.x))
    plt.plot(t, sol[:, 0], 'black')
    plt.plot(t, sol[:, 1], 'red')
    plt.show()
