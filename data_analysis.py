import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution, brute, basinhopping

CC = 40000


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


# TODO: Competitive LV
# I think the objective function is right. We need better data sets

def objective(parameters, *args):
    func, data = args
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    model = np.array(odeint(func, data[0], t, args=tuple(parameters)))
    if model.shape[1] == 1:
        model = model.ravel()
    return np.sum(np.abs(model - data))

if __name__ == '__main__':
    guess_parameters = [0.008, 0.00002, 0.001, 0.001]
    parameters_bounds = ((1e-7, 0.5), (1e-7, 0.1), (1e-7, 0.1), (1e-7, 0.5))
    # TODO: Constraint dictionary

    data = np.loadtxt('pop_data_.csv', delimiter=',')  # [plants, bugs]
    t = np.arange(0, len(data), 1)

    plt.plot(t, data[:, 0], t, data[:, 1])
    # opt_parameters = brute(objective, parameters_bounds, args=(data,))
    opt_parameters = minimize(objective, guess_parameters, args=(lv, data), bounds=parameters_bounds)
    # opt_parameters = basinhopping(objective, guess_parameters, niter=1000, minimizer_kwargs={'args': (data,)})
    print(opt_parameters)

    sol = odeint(lv, data[0], t, args=tuple(opt_parameters.x))
    plt.plot(t, sol[:, 0], 'black')
    plt.plot(t, sol[:, 1], 'red')
    plt.show()
