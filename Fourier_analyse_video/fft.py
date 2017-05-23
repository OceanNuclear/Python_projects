#!/home/oceanw/anaconda3/bin/python3
#This is a miniprogram meant for testing the functionality of the fast fourier transform module in numpy.

import numpy as np
import matplotlib.pyplot as plt

#0. Declare constants
xdim = 1280
seg = int(xdim/3)

#1. Define variables
t = np.arange(xdim/3)

#I want the middle part of the function to go through periods = 8*np.pi angle
mid = np.sin(9*np.pi*t/seg)*np.sin(np.pi*t/seg)
y = np.zeros(seg)

y = np.concatenate((y, mid, y))

#x = np.arange(len(y))
f = np.real(np.fft.rfft(y))
k = np.fft.rfftfreq(len(y))

plt.plot(k, f)
plt.show()
