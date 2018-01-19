#!/home/oceanw/anaconda3/bin/python3

import numpy as np
import matplotlib.pyplot as plt
#import itertools
import matplotlib.colors as colors
#from scipy.interpolate import interp2d
#from scipy.interpolate import Rbf
from matplotlib import cm
from scipy.interpolate import griddata

x, y = np.mgrid[87:346:100j, -255:-40:200j]

r = np.array([87 ,152, 217, 281, 346])
d = np.array([-40, -80, -115, -153, -255])

points = np.zeros((25,2))
for xInd in range (5):
	for yInd in range (5):
		points[xInd*5+yInd] = (r[xInd], d[yInd])

#xi, yi = np.mgrid[r.min():r.max():nbins*1j, d.min():d.max():nbins*1j]
counts = np.array([
	[91401,41859,17363,7052,2632],
	[193607,77909,30294,10794,3500],
	[243079,99569,36304,12632,4273],
	[367465,132203,45761,15225,5017],
	[612040,201294,60789,19417,6249]	])
counts = counts.T.ravel()
#rbf = Rbf(r, d, counts/100, epsilon=2)
#zi = rbf(ri, di)
z = griddata(points, (counts/100), (x, y), method='cubic')

#plt.subplot(1, 1, 1)

fig = plt.figure()
ax = fig.add_subplot(111)
graph = ax.pcolor(x,y,z, cmap=cm.jet)
#plt.scatter(x, y, 100, z, cmap=cm.jet)
ax.set_aspect('equal')
#fig = plt.pcolormesh(x,y,z)

plt.xlim(87,346)
plt.ylim(-255,-40)

plt.xlabel("Radial distance away from source(mm)")
plt.ylabel("Distance from surface of the tank(mm)")
plt.title("Heat Map of Thermal Neutron flux")

plt.colorbar(graph, label = "Count Rate (/s)")

plt.show()
