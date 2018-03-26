#!/home/oceanw/anaconda3/bin/python
#find the scatter within each grain (average misorientation angle from the average orientation), and then save them to the directory of "Scatter/"+average+"/ScatterInGrain"+*+.txt
import numpy as np
from scipy.constants import pi
import matplotlib.pyplot as plt
tau = pi*2
from quat import *
from generalLibrary import *
import time



#23:33:11 I'm trying to race Bash to extract the misorientation in a file.
method = ('sum','each')[1]
average = ('renormalized','min')[1]
numFrame = 397
numGauss = 8
numGrain = 124
misor = np.zeros([numFrame,numGrain])

r = open("Scatter/ScatterOverTimeUniaxial.txt",'r')
time = r.readlines()
for line in range (len(time)):
	time[line] = time[line].split()[0]

f = open( "Scatter/"+average+"/TotalNormalizedScatter.txt", 'w' )
if method == "each":
	Files = ["",]*numGrain
	for grain in range (numGrain):
		Files[grain] = open("Scatter/"+average+"/ScatterInGrain"+str('{:0=3d}'.format(grain+1))+".txt",'w')

for frame in range (numFrame):
	if average == "renormalized":
		meanFileName = "OldExtraction/"+str(frame+1)+"FrameRotationMatrices.txt"
		Means = ReadR(meanFileName)[1:]
	if average == "min":
		meanFileName = "MinimizedMatrices/"+str(frame+1)+"FrameRotationMatrices.txt"
		Means = ReadR(meanFileName)

	everyPointFileName = "LiterallyEveryPoint/"+str(frame+1)+"FrameRotationMatrices.txt"
	Matrices = ReadR(everyPointFileName)

	for grain in range (numGrain):		
		qAvg = RotToQuat(Means[grain])	#Read the average quaternion

		for n in range (numGauss):
			p = RotToQuat(Matrices[grain*numGauss+n])	#Read the specific quaternion
			misor[frame][grain] += misorientation2(p,qAvg)/numGauss	#normalized by number of gauss points within a grain
		if method=="each":
			Files[grain].write(time[frame]+'\t')
			Files[grain].write(str(misor[frame][grain])+'\n')

	print("frame",frame+1,"/", numFrame)
	f.write(time[frame]+"\t")
	f.write(str(np.sum(misor[frame,:])/numGrain)+"\n")	#normalized by total number of points.
	
f.close()
r.close()

if method == "each":
	for grain in range (numGrain):
		Files[grain].close()
