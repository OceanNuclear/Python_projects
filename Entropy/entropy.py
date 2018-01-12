#!/home/oceanw/anaconda3/bin/python3
#Entropy is the measure of surprise, e.g. number of bits required to guess the next word
#This code computes the entropy of a single line txt file input.
#The code below takes a spectrum of counts against channel (counts = how many events with energy E_classmark +/- E_classwidth/2),
#and can be generalized as taking in a histogram and outputting a data.

import numpy as np

inFile = str(input("Please type in the input filename:\n"))
numLines = sum(1 for line in open(inFile))

data=[]
x = []

f = open(inFile, "r")
line=["" for x in range (numLines)]
if (True!=True):
	pass
	'''
	if str(input("Is this file a histogram or raw data? (hist/raw)"))=="hist":
		for n in range (numLines):
			line[n]=(str(f.readline()))
			if (len(line[n].split()) != 1):
				pass
			else:
				data.append( int(line[n].split()[0]) )
		numData=len(data)
		np.histogram(data, bins=int(data.max()-data.min()), density=False)
		hist.sum
	'''
else:
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
print('\n')
print(entropyValue)
print("which is ", 100*entropySum/np.log(numData),"% of the max entropy achievable (", np.log(numData), "), i.e. the data is",(100-100*entropySum/np.log(numData)),"% compressible when transmitted independently.")
print("Expected number of bits (binary unit!) required to encode each datum = ", entropySum/np.log(2))
plt.xlabel("channel")
plt.ylabel("Entropy contribution(unit)")
plt.show()

#So after trimming out the large peaks in Rock.Spe, the entropy increases, i.e. it is more evenly distributed.

#Next step (assuming I have the time) is to find the compressibility of information based on various protocals.
