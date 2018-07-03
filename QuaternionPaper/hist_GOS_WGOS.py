#!/home/oceanw/anaconda3/bin/python3
'''Plots:
1. Histogram of grain volumes
2. GOS against volume
3. WGOS against volume
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.stats import linregress
from generalLibrary import *



frameNo = str(input("(Please input) Plotting frame number = "))
directory = "testModel/"
saveDirectory = "testModelGraphs/"
fileName = ( "Volume_frame"+frameNo,"IntragrainOrientationScatter_frame"+frameNo)
fileName = [directory+name+".txt" for name in fileName]

for inFile in fileName:
	ReadX(inFile)
	if "Volume" in inFile:
		volume = ReadX(inFile)
	elif "Intragrain" in inFile:
		GOS = ReadX(inFile)
WGOS = GOS/volume

fit_x = np.linspace(min(volume), max(volume), 2)

m_GOS, c_GOS, r_GOS, p_GOS, std_err_GOS = linregress(volume, GOS)
GOS_fit = m_GOS*fit_x+c_GOS

m_WGS, c_WGS, r_WGS, p_WGS, std_err_WGS = linregress(volume, WGOS)
WGOS_fit = m_WGS*fit_x + c_GOS

#The commented out code below can be used if I don't need x-labels
'''
fig = plt.figure()	#make blank canvas
ax1 = plt.subplot(311)	#Switch focus onto the 1st plot in the (3,1) layout
plt.hist(volume)
plt.xlabel("grain volume")
plt.ylabel("no. of grains")

ax2 = plt.subplot(312)	#switching focus onto the 2nd plot:
plt.scatter(volume, GOS)
plt.xlabel("degree")
plt.ylabel("Grain orientation scatter(GOS) \n (mean deviation from \n average orientation)")

ax3 = plt.subplot(313)
plt.scatter(volume, WGOS)
plt.xlabel("degree")
plt.ylabel("volume weighted GOS")
'''
fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(3,1)

ax1 = fig.add_subplot(gs[0,:])
ax1.hist(volume)
ax1.set_xlabel("grain volume")
ax1.set_ylabel("no. of grains")

ax2 = fig.add_subplot(gs[1,:])
ax2.scatter(volume, GOS)
ax2.plot(fit_x,GOS_fit)
ax2.set_xlabel("degree")
ax2.set_ylabel("Grain orientation scatter(GOS) \n (mean deviation from \n average orientation)")
ax2.set_title(r"$R^2$ = "+str(r_GOS))

ax3 = fig.add_subplot(gs[2,:])
ax3.scatter(volume, WGOS)
ax3.plot(fit_x,WGOS_fit)
ax3.set_xlabel("degree")
ax3.set_ylabel("volume weighted GOS")
ax3.set_title(r"$R^2$ = "+str(r_WGS))

fig.align_labels()

plt.savefig("test_hist_GOS_WGOS.png")
