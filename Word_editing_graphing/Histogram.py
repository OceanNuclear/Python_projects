#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt
Infile = str(input("What's the data's file name?\n"))
n_data = sum(1 for line in open(Infile))
f = open(Infile, "r")
data = [0 for x in range (n_data)]
for i in range (n_data):
	data[i] = int(f.readline())
plt.hist(data, bins = 100)
plt.show()
