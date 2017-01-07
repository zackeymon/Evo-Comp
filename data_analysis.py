import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize


def lv(population, t, alpha, beta, delta, gamma):
    x, y = population
    dx_dt = x * (alpha - beta * y)
    dy_dt = y * (delta * x - gamma)
    return [dx_dt, dy_dt]

# TODO: Competitive LV
# I think the objective function is right. We need better data sets

def objective(parameters, data):
    sample_size = len(data)
    t = np.arange(0, sample_size, 1)
    lv_model = odeint(lv, data[0], t, args=tuple(parameters))
    return np.sum(np.square(lv_model - data))


if __name__ == '__main__':
    guess_parameters = [0.4, 0.001, 0.001, 0.1]
    parameters_bounds = ((0, None), (0, None), (0, None), (0, None))
    # TODO: Constraint dictionary

    data = np.loadtxt('population_data.csv', delimiter=',')
    t = np.arange(0, len(data), 1)

    plt.plot(t, data[:, 0], t, data[:, 1])

    opt_parameters = minimize(objective, guess_parameters, args=(data,), tol=0.0001, bounds=parameters_bounds)
    print(opt_parameters)
    print(objective(opt_parameters.x, data))

    sol = odeint(lv, data[0], t, args=tuple(opt_parameters.x))
    plt.plot(t, sol[:, 0], t, sol[:, 1])

    plt.show()
