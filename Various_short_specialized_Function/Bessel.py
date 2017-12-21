#!/home/oceanw/anaconda3/bin/python3
#Since nowhere on the internet can I find the zeroth Bessel Function plotted along the Imaginary axis, I shall do it here, on my computer.
#Rationale: I needed this as a solution to the neutron flux distribution around an infinite rod reactor

import numpy as np
from scipy.special import jn
import matplotlib.pyplot as plt
'''
x = np.linspace(-100,100, 10000)
#make an imaginary copy of x
x_2 = np.array(1j*x)

#Calculate the y value and then log-scale it
y = jn(0, x_2)
log_y = np.log(y)

#Has to be plotted with real x values, thus we
plt.plot(x,log_y)
plt.show()
'''

'''Great! We now know that the J_0 ≈ e^|i*x| for xϵℝ 
So this solution of neutron flux is unphysical (i.e. unnormalizable).'''

#Now I will try the solution where L^2 -> -L^2, so to eliminiate the imaginary part of it.
from scipy.special import yn

x = np.linspace(0,100, 1000)
y = jn(0, x)
#b below is the variabel that we're going to tweak
b = 0.5

#Has to be plotted with real x values, thus we
plt.plot(x,jn(0,x))
plt.plot(x,yn(0,x))
plt.show()
#Since y_0 and j_0 are out out phase by pi/2, we can't add them up and get a positive number resulting. Therefore this solution is still unphysical.
