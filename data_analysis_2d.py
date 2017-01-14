import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution
from data_analysis import objective, competitive_lv, CC

data = np.loadtxt('para_fit.csv', delimiter=',')  # [plants, bugs]
x, y = data[:, 0], data[:, 1]
t = np.arange(0, len(data), 1)

plt.plot(t, x, label='food')
plt.plot(t, y, label='bug')
plt.legend()

alpha = 0.193485
gamma = 0.209544

# n_b = 100
# n_d = 100
#
# betas = np.linspace(0.0001, 0.1000, n_b)
# deltas = np.linspace(0.0001, 0.1000, n_d)
#
# obj = np.zeros(shape=(n_d, n_b))
#
# for i in range(n_b):
#     for j in range(n_d):
#         obj[j, i] = objective([betas[i], deltas[j]], competitive_lv, alpha, gamma, data)
#
# print(np.unravel_index(obj.argmin(), obj.shape))
# beta_v, delta_v = np.meshgrid()


guess = [0.01, 0.01]
bounds = ((1e-12, 1.0), (1e-12, 1.0))

# opt = minimize(objective, guess, args=(competitive_lv, alpha, gamma, data), bounds=bounds)
opt = differential_evolution(objective, bounds, args=(competitive_lv, alpha, gamma, data))
print(opt)

actual = [alpha, opt.x[0], opt.x[1], gamma]
sol = odeint(competitive_lv, data[0], t, args=tuple(actual))

plt.plot(t, sol[:, 0], 'black')
plt.plot(t, sol[:, 1], 'red')
plt.show()

