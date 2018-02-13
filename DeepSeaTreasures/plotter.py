#!/home/oceanw/anaconda3/bin/python3
#for debugging:		print( (), type(), len() )
import numpy as np
import matplotlib.pyplot as plt



def removeBrackets(array):
	if np.shape(array)==():
		print(array, "is EMPTY!")
	while ( ( np.shape(array)[0]==1 ) & ( np.ndim(array)>1 ) ):
		array = array[0]
	return array

def lowerBounds_upperBounds(lowerBounds):
	length = len(lowerBounds)
	upperBounds = np.zeros(length)
	for n in range ( length-1 ):
		upperBounds[n] = lowerBounds[n+1]
	upperBounds[length-1] = upperBounds[length-2] - upperBounds[length-3]
	return upperBounds



#Create empty list to store the data read.
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
		grain[x][n][0] = float(grain[x][n][0])
		grain[x][n][1] = float(grain[x][n][1])
	grain[x] = np.transpose(grain[x])
	#grain[x][stress/strain][line]
	#np.shape(grain[x]) = (2,129)

	#plotting:
	#plt.scatter(grain[x][0], grain[x][1], s=1, color='blue', marker = '.')
	strain.append( grain[x][0] )
	stress.append( grain[x][1] )

strain = np.ravel(strain)
stress = np.ravel(stress)

#------------------------------------------------------------HEY LOOK HERE CHANGE THESE VARIABLES TO CHANGE THE PLOTTING DENSITY!_____________________
seg1End = 0.005
seg2End = 0.05
seg3End = 0.067
numBins1 = 80
numBins2 = 100
numBins3 = 10
numBins = numBins1 + numBins2 +numBins3
#------------------------------------------------------------HEY LOOK HERE CHANGE THESE VARIABLES TO CHANGE THE PLOTTING DENSITY!_____________________

strain_lower1 = np.linspace(       0, seg1End, numBins1)
strain_lower2 = np.linspace( seg1End, seg2End, numBins2, endpoint=False); stepSize2 = strain_lower2[1]-strain_lower2[0]
strain_lower3 = np.linspace( seg2End, seg3End, numBins3, endpoint=False); stepSize3 = strain_lower3[1]-strain_lower3[0]

[x+stepSize2 for x in strain_lower2]
[x+stepSize3 for x in strain_lower3]

strain_lower = np.append( strain_lower1, strain_lower2)
strain_lower = np.append( strain_lower , strain_lower3)

strain_upper = lowerBounds_upperBounds(strain_lower)

strain_binsClassMark = (strain_lower+strain_upper)/2

stress_bins = np.zeros(numBins)
scatter = np.zeros(numBins)
sizeBin = np.zeros(numBins)

for Bin in range (numBins):
	#find indices whose strain values falls within the range.
	indices = np.where( (strain>=strain_lower[Bin]) & (strain<strain_upper[Bin]) )
	indices = removeBrackets(indices)
	stressValues = stress[[indices]]

	stress_bins[Bin] = np.mean(stressValues)
	scatter[Bin] = np.std(stressValues)
	sizeBin[Bin] = len(stressValues)

plt.errorbar(strain_binsClassMark, stress_bins, yerr=scatter, fmt = 'o' )
plt.show()
