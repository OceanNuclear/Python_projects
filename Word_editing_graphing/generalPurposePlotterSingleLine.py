#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt

inFile = str( input("File name? (excluding .txt)") )+".txt"
numLines = sum(1 for line in open(inFile))

y = np.zeros(numLines)

f = open(inFile, "r")
f.seek(0)

Data = f.readlines()
f.close()

for line in range (numLines):
	y[line] = Data[line]

#plot You can format it as #'{:0=3.0f}'.format( spectrum*10 )
t = str( "" )
plt.title("Variation of grain orientation over time.")
plt.plot(y, label = t)
plt.legend()
plt.xlabel("Frame")
plt.ylabel("Disorientation")
plt.show()
