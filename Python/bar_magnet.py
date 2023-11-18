import math, itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# set constants
MU_0 = 4 * math.pi * 1e-7
M_0 = 796_000
X_B = 49.5 * 1e-3 / 2
Y_B = 3.003 * 1e-3 / 2
Z_B = 19.954 * 1e-3 / 2

magnet_params = {'M_0': M_0, 'X_B': X_B, 'Y_B': Y_B, 'Z_B': Z_B}

# coordinate mesh
x, y, z = np.meshgrid(np.linspace(-20, 20, 20), np.linspace(-20, 20, 20), np.linspace(-20, 20, 3))


M = magnetisation_field(x, y, z, **magnet_params)
H = magnetic_field_intensity(x, y, z, **magnet_params)
B = MU_0 * (H + M)
