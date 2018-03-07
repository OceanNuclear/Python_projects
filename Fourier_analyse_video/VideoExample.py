#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

fig = plt.figure()
ax = plt.axes(xlim=(0, 60), ylim=(-100,100))	#for lineIn_FTGraphOut: nCo, 2.

def manualInitialize():
	(red, ) = ax.plot([], [], lw=3, color = 'r')
	(green,)= ax.plot([], [], lw=3, color = 'g')
	(blue,) = ax.plot([], [], lw=3, color = 'b')
	(yellow,)=ax.plot([], [], lw=3, color = 'y')
	(white,)= ax.plot([], [], lw=3, color = 'w')#Type of these lines are called "<class 'matplotlib.lines.Line2D'>"
	return (red, green, blue, yellow, white)
(red, green, blue, yellow, white) = manualInitialize()
lineCollection = (red, green, blue, yellow, white)

def animate(i):
	x = np.linspace(0, 20+i , 1234)
	for n in (0,2,4):
		lineCollection[n].set_data(x, (n+1)*10 * np.sin(x + i/(2*np.pi)))
		
	#lineCollection[0].set_ydata( 
	green.set_data([], [])
	yellow.set_data(20*np.cos(x + i/(2*np.pi)), x)
	return lineCollection

def init():
	ax.set_axis_bgcolor((0, 0, 0))
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	fig.set_tight_layout(True)
	return lineCollection

anim = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init, interval=40, blit=True)
plt.show()
#anim.save("VideoExampleOutput.mp4")
