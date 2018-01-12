#!/home/oceanw/anaconda3/bin/python3
#Entropy is the measure of surprise, i.e. number of bits required to guess the next word
#This code computes the entropy of a single line txt file input.
#Currently it is at the stage of deciding the entropy of a list of integers of value (0-29) only by sorting them into 30 bins.

import numpy as np

inFile = str(input("Please type in the input filename:\n"))
numLines = sum(1 for line in open(inFile))

x = []

f = open(inFile, "r")
line=["" for x in range (numLines)]
for n in range (numLines):
	line[n]=(str(f.readline()))
	if (len(line[n].split()) != 1):
		pass
	else:
		x.append( int(line[n].split()[0]) )
numData = len(x) #range of channels
cTotal = sum(x)

entropy = [0.0,]*(numData)
for channel in range (numData):
	px = x[channel]/cTotal
	if(px!=0): entropy[channel] = -px*np.log(px)

entropySum= sum(entropy)

#Results
import matplotlib.pyplot as plt
entropyValue = str("Entropy is measured to be ="+ str(entropySum))
plt.plot(entropy, label=entropyValue)
print(entropyValue)
print("which is ", 100*entropySum/np.log(numData),"% of the max entropy achievable (", np.log(numData), "), i.e. the data is"(100-100*entropySum/np.log(numData))"% compressible")
print("Average number of bits (binary unit!) required to encode each datum = ", entropySum/np.log(2))
plt.xlabel("channel")
plt.ylabel("Entropy contribution(unit)")
plt.show()

#So after trimming out the large peaks in Rock.Spe, the entropy increases, i.e. it is more evenly distributed.

#Next step (assuming I have the time) is to find the compressibility of information based on various protocals.
