#!/home/oceanw/anaconda3/bin/python3
#Purpose of this file is to extract the count rates of various spectra from file. 
#They sums over the whole 2048 channels (where the lower half of the spectrum has been cut-off digitally by Maestro to prevent noise from interfering with the total count rate

import numpy as np
import matplotlib.pyplot as plt

#inFile = str("Aut"+name+".Spe")
r = str(346)
for d in (255,):
	Count = np.zeros(2048)
	inFile = str("Aut9-BF3-600s-1.5kV-32_0-depth-255mm-radial-346mm.Spe")
	numLines = sum(1 for line in open(inFile))

	f = open(inFile, "r")
	f.seek(194)
	#save data
	for channel in range (2048):	
		Count[channel] = int(f.readline())
	print(int(sum(Count)))
	f.close()
'''
#plot
plt.plot(Count, label = str("Depth = "+str(d)+", radial distance="+r))
#can put label 2 = ("total count = ", int(sum(Count)), r'\$pm$', np.sqrt(sum(Count)))
print("total count = ", int(sum(Count)),"	", np.sqrt(sum(Count)))

plt.legend()
plt.xlabel("Channel number")
plt.ylabel("Counts")
plt.show()
'''
