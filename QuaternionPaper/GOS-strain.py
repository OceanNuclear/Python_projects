#!/home/oceanw/anaconda3/bin/python3
'''Extracts the GOS and strain for each grain and plot them against each other.'''
from numpy import *; from numpy import array as ary
import matplotlib.pyplot as plt
from generalLibrary import *



selected = False
if selected: selection = range(1,10)	#specify a smaller list of grain to plot when selected=True.

directory = "testModel/"
saveDirectory = "testModelGraphs/"
strain = ReadX(directory+"Strain.txt")

numFrame = len(strain)
numGrain = len(ReadX(directory+"IntragrainOrientationScatter_frame1.txt"))

GOS = zeros([numFrame, numGrain])	#initiating the variable for GOS

for frame in range (numFrame):
	frameNo = frame+1
	GOS[frame] = ReadX(directory+"IntragrainOrientationScatter_frame"+str(frameNo)+".txt")
if not selected:
	for grain in range (numGrain):
		grainID = grain+1
		t="grain" + str(grainID)
		plt.plot(strain, GOS[:,grain], label = t)
else:
	for grain in selected:
		grainID = grain+1
		t="grain" + str(grainID)
		plt.plot(strain, GOS[:,grain], label = t)

plt.ylabel("Intragrain Misorientation($ ^{o}$)")
plt.xlabel("$\epsilon$")
plt.title("Grain Orientation Scatter(GOS) of individual grain vs Strain")
if selected: plt.legend()	#because the legend will be too long to fit in the graph when EVERY grain is plotted, 
	#we can only afford to put the legedn in when there is a selected list of grain.

plt.savefig(saveDirectory+"individualGOSevolution"+".png")
