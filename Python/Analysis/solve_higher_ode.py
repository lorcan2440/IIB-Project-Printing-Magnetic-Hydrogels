import numpy as np
from scipy.integrate import odeint, solve_ivp, solve_bvp
import matplotlib.pyplot as plt

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

# solve the system of ODEs:
# x_1' = x_2
# x_2' = x_3
# x_3' = x_4
# x_4' = w/EI - 4 * lambda_w * x_1
# subject to boundary conditions
# x_1(-l/2) = 0
# x_1(l/2) = 0
# x_2(-l/2) = 0
# x_2(l/2) = 0

def ode_higher_order(y, x, w, EI, lambda_w):
    x1, x2, x3, x4 = y
    return [x2, x3, x4, w/EI - 4 * lambda_w * x1]

def bc_higher_order(ya, yb, w, EI, lambda_w):
    return [ya[0], yb[0], ya[1], yb[1]]

def solve_higher_ode(w, EI, lambda_w, l):
    x = np.linspace(-l/2, l/2, 100)
    y = solve_bvp(
        fun = lambda x, y: ode_higher_order(y, x, w, EI, lambda_w),
        bc = lambda ya, yb: bc_higher_order(ya, yb, w, EI, lambda_w),
        x = x,
        y = np.zeros((4, x.size))
    )
    return y.sol(x)

# plot the solution for w = 1, EI = 1, lambda_w = 1, l = 1

w = 1
EI = 1
lambda_range = [0, 1, 10, 100]
l = 1

x = np.linspace(-l/2, l/2, 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

for col, lambda_w in zip(['black', 'green', 'gold', 'red'], lambda_range):
    y = solve_higher_ode(w, EI, lambda_w, l)
    ax1.plot(x, 384 * EI * y[0], label=r'$\lambda_w = $ ' + str(lambda_w), color=col)
ax1.legend()
ax1.set_xlabel(r'$\frac{x}{L}$')
ax1.set_ylabel(r'$\frac{y}{y_{max}}$')

y_max = np.array([np.max(np.abs(384 * EI * solve_higher_ode(w, EI, lambda_w, l)[0])) \
                  for lambda_w in np.logspace(-1, 5, 1000, base=10)])

ax2.semilogx(np.logspace(-1, 5, 1000, base=10), y_max)
ax2.set_xlabel(r'$\lambda_w$')
ax2.set_ylabel(r'$\frac{y_{max}}{y_{max, \lambda_w = 0}}$')

plt.show()