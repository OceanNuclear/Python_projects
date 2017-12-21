#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt
x = np.arange(0.02, 2.2, 0.02);
y = 1.471* erf(x/0.7196)
y_wt = 1/(4.65*((100/y)-1) + 1)
y_wt = 100*y_wt
plt.plot(x, y_wt)
plt.ylabel('percentage of C atoms(by weight)')
plt.xlabel('Distance from the surface of the component(cm)')
plt.show()

