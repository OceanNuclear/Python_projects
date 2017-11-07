#!/home/oceanw/anaconda3/bin/python3
#Plot of probability distribution evolution of a normal gaussian wave function with a non-zero average momentum. (Potential = 0)
#Algebaric funciton derived by Bash Mitchell (classmate)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

a = float(input("a=1/2sigma^2= "))
b = float(input("b=(hbar/m)^2= "))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(-2*np.pi, 2*np.pi), ylim=(0, 1))
line, = ax.plot([], [], lw=1)

# initialization function: plot the background of each frame (I didn't touch this part of the code)
def init():
	line.set_data([], [])
	return line,

# animation function
def animate(t):
	x = np.linspace(-2*np.pi, 2*np.pi, int(1000*np.pi))
	y = x-x
	#Calculating the actual displacement at that particular time
	y=np.exp((-a*x*x+b*x*(t/50)-b*b/2*(t/50)*(t/50))/(1+b*b*(t/50)*(t/50)/4))*1/np.sqrt(.5/(a*a)+b*b*(t/50)*(t/50)/2)
		#Using t/50 because the frame rate is 50
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
anim.save('wavefunc_anim'+str(a)+'_'+str(b)+'.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

plt.show()
