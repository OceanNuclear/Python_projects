#!/home/oceanw/anaconda3/bin/python3
#This program extract two particular character from each line of a txt input file and then print them out
import numpy as np
import matplotlib.pyplot as plt

Count = np.zeros(8192)

#name = str(input("What's its name? (ignoring Aut and .Spe)"))
#inFile = str("Aut"+name+".Spe")
inFile = str("Aut6-RockSample.Spe")
numLines = sum(1 for line in open(inFile))
f = open(inFile, "r")
f.seek(194)

#save data
for channel in range (8192):
	Count[channel] = int(f.readline())
f.close()

#plot
plt.semilogy(Count, label = str("Rock Sample"))

Count = np.zeros(8192)

#name = str(input("What's its name? (ignoring Aut and .Spe)"))
#inFile = str("Aut"+name+".Spe")
inFile = str("Aut6-CyclotronShieldingSample.Spe")
numLines = sum(1 for line in open(inFile))
f = open(inFile, "r")
f.seek(194)

#save data
for channel in range (8192):
	Count[channel] = int(f.readline())
f.close()
plt.semilogy(Count, label = str("Cyclotron Shielding material"))

plt.legend()
plt.xlabel("Channel number")
plt.ylabel("Counts")
plt.show()
