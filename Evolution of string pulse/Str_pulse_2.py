#!/home/oceanw/anaconda3/bin/python3
#An attempt to model the time evolution of a pulse of a particular shape on a string

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import scipy.integrate as inte

n_max = int(input("Number of coefficients to analyze up to (every 2 coef. takes ~1 second to compute): "))
A = [0]*(n_max+1)
for_bound = n_max+1
#n_max+1 because 0 is not used.

#I won't let the user to define the curve itself yet, afterall it can be done easily inside this .py code
#The paragraph below only outlines the shape of the curve on the left side of the sine. The end result will assume this shape is rotated 180 degree at x = pi on the x-axis.
X = [np.pi]*6
Y = [0]*6
#General boundary condition
X[0] = 0
#Y[0] = 0
#X[5] = np.pi
#Y[5] = 0

#User specified boundary conditions:
for i in range (1,5):
	X[i] = input("X["+str(i)+"]/pi=")
	if X[i] == '' : 
		X[i]=np.pi
		break
	X[i] = float(X[i])*np.pi
	Y[i] = input("Y["+str(i)+"]=")
	Y[i] = float(Y[i])
#Initialize the functions
Y_1 = [0]*(n_max+1)
Y_2 = [0]*(n_max+1)
Y_3 = [0]*(n_max+1)
Y_4 = [0]*(n_max+1)
Y_5 = [0]*(n_max+1)
#n_max + 1 because 0 is not used

#for i in range (0, 6):
for n in range (1,for_bound):
	Y_1[n] = lambda x : np.sin(n*x) * (Y[1] + (x - X[1])*(Y[1]-Y[0])/(X[1]-X[0]))
	if (X[2]>X[1]):
		Y_2[n] = lambda x : np.sin(n*x) * (Y[2] + (x - X[2])*(Y[2]-Y[1])/(X[2]-X[1]))
	else: Y_2[n] = lambda x : 0
	if (X[3]>X[2]):
		Y_3[n] = lambda x : np.sin(n*x) * (Y[3] + (x - X[3])*(Y[3]-Y[2])/(X[3]-X[2]))
	else: Y_3[n] = lambda x : 0
	if (X[4]>X[3]):
		Y_4[n] = lambda x : np.sin(n*x) * (Y[4] + (x - X[4])*(Y[4]-Y[3])/(X[4]-X[3]))
	else: Y_4[n] = lambda x : 0
	if (X[5]>X[4]):
		Y_5[n] = lambda x : np.sin(n*x) * (Y[5] + (x - X[5])*(Y[5]-Y[4])/(X[5]-X[4]))
	else: Y_5[n] = lambda x : 0

# Fourier analyse to get coefficients
for n in range (1,for_bound):
	A[n] += (1/np.pi)*inte.quad(Y_1[n], X[0], X[1])[0]
	A[n] += (1/np.pi)*inte.quad(Y_2[n], X[1], X[2])[0]
	A[n] += (1/np.pi)*inte.quad(Y_3[n], X[2], X[3])[0]
	A[n] += (1/np.pi)*inte.quad(Y_4[n], X[3], X[4])[0]
	A[n] += (1/np.pi)*inte.quad(Y_5[n], X[4], X[5])[0]
	#Integrate through all 2pi
#and repeat for each orthorgonal sine function in n.
A = 2*A #multiplied by two because the function is rotationally symmetric at x = pi.

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2*np.pi), ylim=(-1, 1))
line = ax.plot([], [], lw=3)

# initialization function: plot the background of each frame (I didn't touch this part of the code)
def init():
	line.set_data([], [])
	return line,

# animation function
def animate(t):
	x = np.linspace(0, 2*np.pi, int(1000*np.pi))
	y = x-x
	#Calculating the actual displacement at that particular time
	for n in range (1, for_bound):
		if (abs(A[n])>0.0001):
			y +=  A[n] *np.sin(n*x) *np.cos(n*t/50)
	line.set_data(x, y)
	return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=int(100*np.pi), interval=50, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('temp'+str(n_max)+'.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

plt.show()
