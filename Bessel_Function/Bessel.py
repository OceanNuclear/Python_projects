#!/home/oceanw/anaconda3/bin/python3
#Since nowhere on the internet can I find the zeroth Bessel Function plotted along the Imaginary axis, I shall do it here, on my computer.
#Rationale: I needed this as a solution to the neutron flux distribution around an infinite rod reactor

import numpy as np
from scipy.special import jn
import matplotlib.pyplot as plt
x = np.linspace(-100,100, 10000)
#make an imaginary copy of x
x_2 = np.array(1j*x)

#Calculate the y value and then log-scale it
y = jn(0, x_2)
log_y = np.log(y)

#Has to be plotted with real x values, thus we
plt.plot(x,log_y)
plt.show()

'''Great! We now know that the J_0 ≈ e^|i*x| for xϵℝ 
So this solution of neutron flux is unphysical (i.e. unnormalizable).'''
