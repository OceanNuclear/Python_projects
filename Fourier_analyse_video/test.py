#!/home/oceanw/anaconda3/bin/python3
import matplotlib.pyplot as plt
import numpy as np

def plot2(W):
	x = np.arange(len(W))
	plt.plot(x, W)
	plt.show()
