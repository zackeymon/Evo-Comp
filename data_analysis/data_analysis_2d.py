import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from data_analysis import objective_2d, competitive_lv, CC

data = np.loadtxt('para_fit_.csv', delimiter=',')  # [plants, bugs]
x, y = data[:, 0], data[:, 1]
t = np.arange(0, len(data), 1)

plt.plot(t, x, '.',  label='Plants')
plt.plot(t, y,  '.', label='Bugs')

plt.xlabel('Time + 1421')
plt.ylabel('Population')
plt.title('World Population')


alpha = 0.193485
gamma = 0.209544

guess = [5.02921384e-05, 6.85824820e-05]
bounds = ((4e-05, 6e-05), (6e-05, 7e-05))

opt = minimize(objective_2d, guess, args=(competitive_lv, alpha, gamma, data), bounds=bounds)
print(opt)

actual = [alpha, opt.x[0], opt.x[1], gamma]
sol = odeint(competitive_lv, data[0], t, args=tuple(actual))

plt.plot(t, sol[:, 0], 'black', label='Plants Fit')
plt.plot(t, sol[:, 1], 'red', label='Bugs Fit')
plt.legend(loc=0)
plt.savefig('ltv_analysis.png')
plt.show()
