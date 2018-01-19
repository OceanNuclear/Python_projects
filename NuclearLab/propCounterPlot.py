#!/home/oceanw/anaconda3/bin/python3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.

X = np.arange(0, 1, 0.05)
Y = np.arange(0, 1, 0.5)
X, Y = np.meshgrid(X, Y)

Data = [np.zeros(20),]*2
Data[0] = [0,0.107680359,0.15606114,0.15606114,0.15606114,0.15606114,0.164956729,0.197168161,0.259029382,0.347841694,0.455186755,0.562531817,0.669876878,0.777221939,0.829649137,0.858489643,0.887330148,0.930771473,0.974212798,1.017654123]
Data[1] = [0,0.184500268,0.270620407,0.270620407,0.270620407,0.270620407,0.294337628,0.342721672,0.426146376,0.523044994,0.589621595,0.656198196,0.722774797,0.789351399,0.829649137,0.858489642,0.887330148,0.930771473,0.974212798,1.017654123]
Z = Data

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])
ax.axes.zaxis.set_ticklabels([])
ax.axes.set_xlabel("Applied Voltage")
ax.axes.set_ylabel(r"$E_\gamma$(keV)")
ax.axes.set_zlabel("log(pulse amplitude)")
ax.auto_scale_xyz([0, 1], [0, 10], [0, 1])
ax.pbaspect = [10, 1, 10]
# Add a color bar which maps values to colors.
cbar = fig.colorbar(surf, ticks=[])

ax.view_init(40, 270)
plt.show()
