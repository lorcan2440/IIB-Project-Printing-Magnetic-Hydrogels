import numpy as np
import matplotlib.pyplot as plt

# data for the Young's modulus [MPa] (3rd column) of a 
# hydrogel with percent alginate (1st column) and 
# percent gelatin (2nd column)
# taken from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9499472/, Table 1
data = [
    [7, 0, 4.93],
    [8, 0, 2.08],
    [9, 0, 6.09],
    [7, 3, 2.04],
    [3, 7, 0.83],
    [7, 0, 1.47],
    [7, 3, 2.00],
    [3, 7, 0.36],
    [0, 15, 0.04556],
    [0, 25, 0.07655],
    [0, 10, 0.07],
    [0, 15, 0.08],
]

# want to estimate the Young's modulus of a hydrogel with
# 1% alginate and 6% gelatin

from sklearn.linear_model import LinearRegression

data = np.array(data)
x = data[:, :2]
y = data[:, 2]

# use order 2 polyfit

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

model = make_pipeline(PolynomialFeatures(2), LinearRegression())
model.fit(x, y)

# estimate the Young's modulus of a hydrogel with 1% alginate and 6% gelatin
y_pred_1 = model.predict([[1, 6]])
y_pred_2 = model.predict([[0.333, 2]])
print(y_pred_1)
print(y_pred_2)

# plot the data in 3D and the surface of the fitted model
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data[:, 0], data[:, 1], data[:, 2])

x = np.linspace(0, 10, 100)
y = np.linspace(0, 30, 100)
x, y = np.meshgrid(x, y)
z = model.predict(np.column_stack((x.ravel(), y.ravel()))).reshape(x.shape)
ax.plot_surface(x, y, z, alpha=0.5)

# mark the predicted point in red
ax.scatter(1, 6, y_pred_1, color='red')
ax.scatter(0.333, 2, y_pred_2, color='red')

# print RMSE
from sklearn.metrics import mean_squared_error
print(np.sqrt(mean_squared_error(model.predict(data[:, :2]), data[:, 2])))


ax.set_xlabel('Percent alginate')
ax.set_ylabel('Percent gelatin')
ax.set_zlabel('Young\'s modulus [MPa]')
plt.show()

