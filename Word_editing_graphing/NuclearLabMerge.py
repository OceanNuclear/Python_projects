#!/home/oceanw/anaconda3/bin/python3
# This program plots two spectra overlayed of one another.
import numpy as np
import matplotlib.pyplot as plt

#Chosen = [0,4,8,11]
#Min=0
#Max=1

Count = [np.zeros(8192),]*(2)
inFile = ["",]*(2)

for spectrum in range (2):
	inFile[spectrum] = str("Unknown-Sample-"+'{:0=1.0f}'.format( spectrum+1 )+"-30mins"+".Spe")
	numLines = sum(1 for line in open(inFile[spectrum]))
	f = open(inFile[spectrum], "r")
	f.seek(194)

	#save data
	for channel in range (8192):
		Count[spectrum][channel] = int(f.readline())
	
	#plot
	plt.plot(Count[spectrum], label = str("sample"+str(spectrum+1)))
plt.legend()
plt.xlabel("Channel number")
plt.ylabel("Counts")
plt.show()
