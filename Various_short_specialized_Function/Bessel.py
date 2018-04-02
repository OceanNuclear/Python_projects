#!/home/oceanw/anaconda3/bin/python3
#Since nowhere on the internet can I find the zeroth Bessel Function plotted along the Imaginary axis, I shall do it here, on my computer.
#Rationale: I needed this as a solution to the neutron flux distribution around an infinite rod reactor

#Parametrically plots the e^(e^i*theta)) graph
from numpy import e, cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import matplotlib.pyplot as plt
from scipy.special import jn, yv
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
b = 3
x = np.linspace(0.001,1000, 10000)+b*1j
#b below is the variabel that we're going to tweak

'''
#Has to be plotted with real x values, thus we
plt.plot(x,jn(0,x))
plt.plot(x,yv(0,x))
'''
#plt.plot(np.real(yv(0,x)),np.real(jn(0,x)),label = "Real of second kind \n against real of first kind")
#plt.plot(np.real(jn(0,x)),np.imag(jn(0,x)),label = "second kind complex")
plt.plot(np.real(yv(0,x)),np.imag(yv(0,x)),label = "first kind complex")
plt.legend()
plt.suptitle("Bessel Functions plotted")
plt.title(r"on $\mathbb{C}$ for $\mathbb{R} >0$ along the height of complex="+str(b)+"i")
plt.show()
#Since y_0 and j_0 are out out phase by pi/2, we can't add them up and get a positive number resulting. Therefore this solution is still unphysical.
