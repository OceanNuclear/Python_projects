#!/home/oceanw/anaconda3/bin/python3
#Since nowhere on the internet can I find the zeroth Bessel Function plotted along the Imaginary axis, I shall do it here, on my computer.
#Rationale: I needed this as a solution to the neutron flux distribution around an infinite rod reactor

import numpy as np
import scipy.special.jn as jn
import matplotlib.pyplot as plt
x = np.linspace(0,100, 10000)
x = np.array(1j*x)
y = jn(0, x)
plt.plot(x,y)
plt.show()
