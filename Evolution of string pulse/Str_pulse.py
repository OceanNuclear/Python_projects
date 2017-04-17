#!/home/oceanw/anaconda3/bin/python3
#An attempt to model the time evolution of a pulse of a particular shape on a string

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

n_max = int(input("Number of coefficients to analyze up to: "))
A = [0]*(n_max+1)
#To be replaced with fourier analysis
for i in range (0, 30):
	A[2*i+1] = 2*pow(-1, i)/(pow((2*i+1),2)*np.pi)

'''
#Let the user input up to 5 points for connecting them up into a graph

for
	input (?)

#1 (Optional): Fourier analyse it
A= []
for x in range (1,n_max):
	cosfunc = lambda x : np.cos(x**2)
	A.append
'''

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 3.14), ylim=(-1, 1))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
	line.set_data([], [])
	return line,

# animation function.  This is called sequentially
def animate(t):
	x = np.linspace(0, 3.14, 3141)
	y = A[1]* np.sin(x)* np.cos(t/50)
	#Calculating the actual displacement at that particular time
	for n in range (2, n_max):
		y= y + A[n] *np.sin(n*x) *np.cos(n*t/50)
	line.set_data(x, y)
	return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=314, interval=50, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
coef=str(n_max)
anim.save('halfwave'+str(n_max)+'.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

plt.show()
