#!/home/oceanw/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt;
from numpy import array as ary;
import numpy as np;
tau = 2*pi
from quat import*
from generalLibrary import *
import random as rn
import matplotlib.pyplot as plt



folder = "seed_1/"
rn.seed(1)
def randomQGenerator():
	w = rn.uniform(1,0)		#pick a random angle of rotation
	THETA = arccos(rn.uniform(-1,1))#pick a random THETA, and make sure to scale it appropriately.
	PHI = rn.uniform(0, tau)	#pick a random PHI

	st2 = sqrt(1-w**2)
	x,y,z = spherical_cartesian(THETA,PHI)
	return ary([w, st2*x, st2*y, st2*z])

'''Draws the pole figure, don't touch!!!██████████████████████████████████████████████████████████████████████████████████████'''
global fig
fig = plt.figure()
fig.set_tight_layout(True)	#remove the black outline.

global ax
ax = plt.subplot(111)
#ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.axis('off')

xlimits = expandAxisLimit(0, tan(pi/8) )
ylimits = expandAxisLimit(0,0.366)
ax.set_xlim(xlimits)
ax.set_ylim(ylimits)

ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect(0.366/tan(pi/8))

X_ipf,Y_ipf = InversePoleFigureLine()
ax.plot(X_ipf,Y_ipf, color='black')#, lw=0.8

ax.annotate("[001]",	xy=[0,0], xycoords='data', ha='right',	color = 'black')
ax.annotate("[101]",	xy=[tan(pi/8),0],xycoords='data',	color = 'black')
x_an, y_an = getIPtip()
ax.annotate("[111]",	xy=[x_an,y_an],	xycoords='data',	color = 'black')

'''End of pole figure generation code.████████████████████████████████████████████████████████████████████████████████████████'''
ax.set_title("Random Orientations")

f = open(folder+"orientationMatrix.txt", 'w')

for grain in range(27):
	q = randomQGenerator()
	'''<Standard code to turn rotation rotation matrices>██████████████████████████████████████████████████████████████████'''
	v48 = duplicate48Points(Q_v(q)[0], Q_v(q)[1], Q_v(q)[2])
	r = chooseIPpoint(v48)
	#ID[grain] = getIPpointID(v48)	#optional
	[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])
	R, Angle = stereographicProjector(Theta,Phi)
	X, Y = polar2D_xy(Angle, R)

	ax.scatter(X, Y , color = 'black', marker = 'x')
	'''<\Standard code to turn quaternion into IPF (inverse pole figure)>█████████████████████████████████████████████████'''
	#ax.plot(X2,Y2, markeredgecolor = 'black', markerfacecolor = 'none', marker='x')
	ax.annotate(chr(65+grain),xy=(X, Y), xycoords='data', color='r', fontname='DejaVu Sans Mono')	#Make annotation directly next to the point being plotted.
	
	f.write(writeMatrix(QuatToR(q)))	#write the rotation matrix to file.

f.close()
plt.savefig(folder+"poleFigure.png")
