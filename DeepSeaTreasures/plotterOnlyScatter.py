#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm



grain = ["",]*125
stress = []
strain = []

for x in range (0,125):
	#opening file
	grainNum= x+1
	inFile = "GRAIN_"+ str(grainNum) +".txt"
	numLines = sum(1 for line in open(inFile))
	#if numLines!= 129: print("File",grainNum,"has",numLines,"lines instead of 129 lines, there may be potential problems down the line!")
	f = open(inFile, "r")
	grain[x] = f.readlines()
	f.close()

	#convert data obtained into grain[x][stress/strain][line]
	for n in range (numLines):
		grain[x][n] = grain[x][n].split()
	grain[x] = np.transpose(grain[x])
	#grain[x][stress/strain][line]

	#plotting
	plt.scatter(grain[x][0], grain[x][1], s=1, color='blue', marker = '.')
	strain.append( grain[x][0] )
	stress.append( grain[x][1] )
plt.show()

for x in range (0,125):
	plt.scatter(grain[x][0], grain[x][1])
	plt.title("GRAIN"+str(x+1))
	plt.show()

#The code below demonstrate how to colour a single curve with multiple colours. I've given up on figuring out how it works.

'''
x = np.linspace(0, 3 * np.pi, 500)
y = np.sin(x)
z = np.cos(0.5 * (x[:-1] + x[1:]))  # first derivative

# Create a colormap for red, green and blue and a norm to color
# f' < -0.5 red, f' > 0.5 blue, and the rest green
cmap = ListedColormap(['red', 'orange', 'blue', 'brown'])
norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)

# Create a set of line segments so that we can color them individually
# This creates the points as a N x 1 x 2 array so that we can stack points
# together easily to get the segments. The segments array for line collection
# needs to be numlines x points per line x 2 (x and y)
points = np.array([x, y]).T.reshape(-1, 1, 2)#reshape it into a matrix of shape with max index of [len(x)][0][1]
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create the line collection object, setting the colormapping parameters.
# Have to set the actual values used for colormapping separately.
lc = LineCollection(segments, cmap=cmap, norm=norm)
lc.set_array(z)
lc.set_linewidth(3)
plt.gca().add_collection(lc)

plt.xlim(x.min(), x.max())
plt.ylim(-1.1, 1.1)
plt.show()
'''
