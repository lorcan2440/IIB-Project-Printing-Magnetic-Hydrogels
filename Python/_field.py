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

def get_field_vector_3d(x: float, y: float, z: float,
        M_0: float = M_0, X_B: float = X_B, Y_B: float = Y_B, Z_B: float = Z_B,
        allow_magnet_boundaries: bool = False) -> tuple:

    '''
    Inputs:

    `x, y, z`: position vector, relative to (0, 0, 0) as the geometric centre of the magnet, at which
    to calculate the magnetic flux density vector. Units: metre

    `M_0`: remanent magnetisation. Units: amps per metre

    `X_B, Y_B, Z_B`: half-dimensions of the magnet along the x, y, z axes. Units: metre

    Outputs:

    `(B_x, B_y, B_z)`: B-field vector attached to input point. Units: Tesla

    Returns the magnetic flux density vector (B_x, B_y, B_z) at a given point (x, y, z).
    Calculates for a cuboid-shaped bar magnet with its geometric centre at (0, 0, 0).
    The North and South poles are along the positive and negative y-axes respectively.

    NOTE: Undefined at the surfaces of the magnet - blows up to infinite magnitude.
    NOTE: Derivative of B_y is discontinuous.

    Equation source: https://aip.scitation.org/doi/full/10.1063/1.1883308; page 2; eq. 5-7.
    '''

    scale_factor = M_0 / (4 * math.pi)
    sum_x = sum_y = sum_z = 0
     
    try:
        for (k, l, m) in itertools.product((1, 2), repeat=3):
            # substitutions
            t = (-1)**(k + l + m)
            h_x = x + (-1)**k * X_B
            h_y = y + (-1)**l * Y_B
            h_z = z + (-1)**m * Z_B
            s = math.sqrt(h_x**2 + h_y**2 + h_z**2)
            # calculate summation expressions
            sum_x += t * math.log(h_z + s)
            sum_y += t * (h_x * h_y / (abs(h_x) * abs(h_y))) * math.atan((abs(h_x) / abs(h_y)) * (h_z / s))
            sum_z += t * math.log(h_x + s)

    except ZeroDivisionError:
        if allow_magnet_boundaries:
            return
        else:
            raise ZeroDivisionError('The magnetic flux density on the boundary of the magnet is discontinuous.'
                f'The point ({x}, {y}, {z}) cannot be evaluated.')

    else:
        H_x = scale_factor * sum_x
        H_y = -1 * scale_factor * sum_y
        H_z = scale_factor * sum_z
    
    return (H_x, H_y, H_z)

def get_field_vector_2d(x: float, y: float,
     M_0: float = M_0, X_B: float = X_B, Y_B: float = Y_B, Z_B: float = Z_B,
     allow_magnet_boundaries: bool = False) -> tuple:

     '''
     Inputs:

     `x, y`: position vector, relative to (0, 0, 0) as the geometric centre of the magnet, at which
     to calculate the magnetic flux density vector. Units: metre

     `M_0`: remanent magnetisation. Units: amps per metre

     `X_B, Y_B, Z_B`: half-dimensions of the magnet along the x, y, z axes. Units: metre

     Outputs:

     `(B_x, B_y)`: B-field vector attached to input point. Units: Tesla

     Returns the magnetic flux density vector (B_x, B_y) at a given point (x, y).
     Calculates for a cuboid-shaped bar magnet with its geometric centre at (0, 0, 0).
     The North and South poles are along the positive and negative y-axes respectively.

     NOTE: Undefined at the surfaces of the magnet - blows up to infinite magnitude.
     NOTE: Derivative of B_y is discontinuous.
     '''

     scale_factor = MU_0 * M_0 / (4 * math.pi)
     sum_x = sum_y = 0
     
     try:
          for (k, l, m) in itertools.product((1, 2), repeat = 3):
               # substitutions
               t = (-1)**(k + l + m)
               h_x = x + (-1)**k * X_B
               h_y = y + (-1)**l * Y_B
               h_z = (-1)**m * Z_B
               s = math.sqrt(h_x**2 + h_y**2 + h_z**2)
               # calculate summation expressions
               sum_x += t * math.log(h_z + s)
               sum_y += t * (h_x * h_y / (abs(h_x) * abs(h_y))) * math.atan((abs(h_x) / abs(h_y)) * (h_z / s))

     except ZeroDivisionError:
          if allow_magnet_boundaries:
               return
          else:
               raise ZeroDivisionError('The magnetic flux density on the boundary of the magnet is discontinuous.'
                    f'The point ({x}, {y}) cannot be evaluated.')

     else:
          B_x = scale_factor * sum_x
          B_y = -1 * scale_factor * sum_y
          
          return (B_x, B_y)

def draw_cuboid(pos=(0, 0, 0), size=(1, 1, 1), ax=None, **kwargs):

     '''
     Inputs:

     `pos`: (x, y, z) coordinate of corner with smallest values

     `size`: edge lengths along positive (x, y, z) axes

     Sourced from:
     https://stackoverflow.com/a/49281004/8747480
     '''

     if ax is not None:

          l, w, h = size
          o = pos

          x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]], [o[0], o[0] + l, o[0] + l, o[0], o[0]],
               [o[0], o[0] + l, o[0] + l, o[0], o[0]], [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
          y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]], [o[1], o[1], o[1] + w, o[1] + w, o[1]],
               [o[1], o[1], o[1], o[1], o[1]], [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
          z = [[o[2], o[2], o[2], o[2], o[2]], [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
               [o[2], o[2], o[2] + h, o[2] + h, o[2]], [o[2], o[2], o[2] + h, o[2] + h, o[2]]]

          x, y, z = np.array(x), np.array(y), np.array(z)
          ax.plot_surface(x, y, z, rstride=1, cstride=1, **kwargs)

def draw_magnet(X_B: float = X_B, Y_B: float = Y_B, Z_B: float = Z_B):

     '''
     Draws two coloured cuboids representing the magnet's North (red) and South (grey) poles.
     Requires a set of 3D axes:
     
     `from mpl_toolkits.mplot3d import Axes3D; 
     ax = fig.add_subplot(111, projection=Axes3D.name)`
     
     to be already set before calling.

     Inputs:

     `X_B, Y_B, Z_B`: half-dimensions of the magnet along the x, y, z axes
     '''

     if ax.name == '3d':
          positions = [(-X_B, -Y_B, -Z_B), (-X_B, 0, -Z_B)]
          sizes = [(2 * X_B, Y_B, 2 * Z_B), (2 * X_B, Y_B, 2 * Z_B)]
          colors = ['gray', 'crimson']

          for p, s, c in zip(positions, sizes, colors):
               draw_cuboid(pos=p, size=s, ax=ax, color=c)

     else:
          ax.add_patch(patches.Rectangle((-X_B, -Y_B), 2 * X_B, Y_B, fill=True, color='gray'))
          ax.add_patch(patches.Rectangle((-X_B, 0), 2 * X_B, Y_B, fill=True, color='red'))










# example applications
if __name__ == '__main__':

     print(get_field_vector_3d(0, 0, 0))

     # draw magnet with field illustration
     fig = plt.figure()
     ax = fig.add_subplot(111, projection=Axes3D.name)
     B = np.vectorize(get_field_vector_3d)
     x, y, z = np.meshgrid(np.linspace(-20, 20, 20), np.linspace(-20, 20, 20), np.linspace(-20, 20, 3))
     u, v, w = B(x, y, z)
     ax.quiver(x, y, z, u, v, w, arrow_length_ratio = 0.25, normalize = True, color = 'black')
     draw_magnet()
     ax.set_xlabel('$x$')
     ax.set_ylabel('$y$')
     ax.set_zlabel('$z$')
     plt.show()

     # plot field strength
     y_pos = np.linspace(-20, 20, 100)
     b_vals = np.array(list(map(lambda y: B(0, y, 0)[1], y_pos)))
     plt.plot(y_pos, b_vals)
     plt.xlabel('distance along $y$-axis')
     plt.ylabel('magnetic flux density')
     plt.show()

     # draw 2D field lines, in plane z = 0
     fig = plt.figure()
     ax = fig.add_subplot(111)
     B = np.vectorize(get_field_vector_2d)
     x, y = np.meshgrid(np.linspace(-20, 20, 10), np.linspace(-20, 20, 10))
     u, v = B(x, y)
     color = 2 * np.log(np.hypot(u, v))
     stream = ax.streamplot(x, y, u, v, color=color, linewidth=1, cmap=plt.cm.inferno, density=2, arrowstyle='->', arrowsize=1.5)
     draw_magnet()
     ax.set_xlabel('$x$')
     ax.set_ylabel('$y$')
     ax.set_xlim((-20, 20))
     ax.set_ylim((-20, 20))
     ax.set_aspect('equal')
     fig.colorbar(stream.lines, label='magnetic flux density $|\mathbf{B}|$, mT')
     plt.show()
