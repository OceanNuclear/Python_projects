#!/home/oceanw/anaconda3/bin/python3
import numpy as np

def func(x, y):
	return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2
x, y = np.mgrid[0:1:100j, 0:1:200j]
points = np.random.rand(1000, 2)
print(np.shape(points))
values = func(points[:,0], points[:,1])
from scipy.interpolate import griddata
grid_z0 = griddata(points, values, (x, y), method='nearest')
grid_z1 = griddata(points, values, (x, y), method='linear')
grid_z2 = griddata(points, values, (x, y), method='cubic')
print(np.shape(x))
print(np.shape(grid_z2))


import matplotlib.pyplot as plt
plt.subplot(221)
plt.imshow(func(x, y).T, extent=(0,1,0,1), origin='lower')
plt.plot(points[:,0], points[:,1], 'k.', ms=1)
plt.title('Original')
plt.subplot(222)
plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
plt.title('Cubic')
plt.gcf().set_size_inches(6, 6)
plt.show()
