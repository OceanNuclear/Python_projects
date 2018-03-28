#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt

inFile = str( input("File name? (excluding .txt)") )+".txt"
numLines = sum(1 for line in open(inFile))
xlabel = str(input("x axis label?"))
ylabel = str(input("y axis label?"))
Title = str( input("Title?"))
label = str( input("Line label?"))

x = np.zeros(numLines)
y = np.zeros(numLines)

f = open(inFile, "r")
f.seek(0)

Data = f.readlines()
f.close()

for line in range (numLines):
	x[line] = Data[line].split()[0]
	y[line] = Data[line].split()[1]

#plot You can format it as #'{:0=3.0f}'.format( spectrum*10 )
t = str(label)
plt.plot( x, y, label = t)
plt.title(Title)
#plt.legend()
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.show()
