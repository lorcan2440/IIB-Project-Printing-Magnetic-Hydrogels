import numpy as np
from matplotlib import pyplot as plt

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

# function for F_mag / (N * I * mu_0 * M_0)
F_norm = lambda x, R, L: -4 * np.pi * R ** 4 * (
    ((L + 2 * x) ** 2 + 4 * R ** 2) ** (-3/2) - \
    ((L - 2 * x) ** 2 + 4 * R ** 2) ** (-3/2)
)

# plot F_norm(x/L) for different ratios of R/L
L = 1
R_vals = [0.5, 0.75, 1, 1.5, 2]
x_range = np.linspace(L/2, 5*L/2, 1000)

for R in R_vals:
    plt.plot(
        x_range, F_norm(x_range, R, L), label=r'$\frac{R}{L} = $ ' + f'{R}')
plt.xlim((0, 5*L/2))
plt.xlabel(r'$\frac{z}{L}$')
plt.ylabel(r'$\frac{-F_{\text{mag}}}{N \cdot I \cdot \mu_0 \cdot M_0}$')
plt.legend()
plt.show()