#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
import numpy as np
import scipy.constants as k
e = 2.718281828
t_n = 1001
t = np.linspace(0,10,t_n)
t = np.linspace(0,2*k.pi,t_n)
x = e**(np.cos(t))*np.cos(np.sin(t))
y = e**(np.cos(t))*np.sin(np.sin(t))
import matplotlib.pyplot as plt
plt.plot(x,y)
plt.show()
