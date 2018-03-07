#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.transforms import Affine2D, Bbox, TransformedBbox
#Colours!
color	= 3
cList   = ('red','green','blue','yellow','white')
outColor= len(cList)
R,G,B,Y,W = np.arange(outColor)
#Used in this particular program:
nCo	= 60	#number of coefficient in fourier analysis
thresold= 0.1 #if more than this fraction of c-colored line is missing, then it is considered invalid as a line.



fig = plt.figure(frameon=False) #this implicitly is equal to
#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)

fig.set_size_inches(8,6)	#implies fig.set_tight_layout(True)
ax = plt.Axes(fig, [0., 0., 1., 1.] )
fig.add_axes(ax)

ax.set_axis_bgcolor((0, 0, 0))
ax.set_xlim(0,nCo)	#equivalent to
ax.set_ylim(-100,100)	#ax = plt.axes(xlim=(0, nCo), ylim=(-100,100))
#ax.set_axis_off() #pedantically double checks that the axes are off

(red, ) = ax.plot([1,2], [3,4], lw=3, color = 'r')
(green,)= ax.plot([8,7], [6,5], lw=3, color = 'g')
(blue,) = ax.plot([9,20], [11,23], lw=3, color = 'b')
(yellow,)=ax.plot([60,23], [100,34], lw=3, color = 'y')
(white,)= ax.plot([34,4], [1,2], lw=3, color = 'w')#Type of these lines are called "<class 'matplotlib.lines.Line2D'>"
lineCollection = (red, green, blue, yellow, white)

fig.savefig("SeamlessFigureTesting.png")
