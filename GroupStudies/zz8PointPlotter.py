#!/home/oceanw/anaconda3/bin/python
import numpy as np
from scipy.constants import pi
import math
import matplotlib.pyplot as plt
from numpy import sin, cos, tan, arccos, arctan, sqrt
from quat import *
tau = pi*2
from quat import *
from matplotlib import animation
from generalLibrary import *



#Background plotting functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle=':')
	return [R,Angle]

def plotDiag(phi):
	X,Y=polar2D_xy([phi,]*2, [0,1])
	ax.plot( X,Y , color='black', linestyle=':')
	return

def plotDiag2(phi):
	X,Y=polar2D_xy([phi,]*2, [pi/6,1])
	ax.plot( X,Y , color='g')
	return

def BGIP():
	X,Y = InversePoleFigureLine()
	ax.plot(X, Y, color='black')

	s3 = sqrt(1/3)
	theta_an, phi_an = cartesian_spherical(s3,s3,s3)
	R_an, Angle_an = stereographicProjector(theta_an, phi_an)
	x_an, y_an = polar2D_xy( Angle_an, R_an )
	
	ax.annotate("[001]",	xy=[0,0], xycoords='data', ha='right',	color = 'black')
	ax.annotate("[101]",	xy=[tan(pi/8),0],xycoords='data',	color = 'black')
	ax.annotate("[111]",	xy=[x_an,y_an],	xycoords='data',	color = 'black')
	return []
''' #unuesd program, left here for reference.
def BG():
	for n in range (3):
		plotCircle(pi/4, n*tau/4)

	R, Phi = drawHalfCircle(pi/4, pi)

	EdgeR, EdgeA = 0, 0

	EdgeR = np.append(EdgeR, R)
	EdgeA = np.append(EdgeA, Phi)

	EdgeR = np.append(EdgeR, 0)
	EdgeA = np.append(EdgeA, pi/4)

	X,Y = polar2D_xy(EdgeA,EdgeR)
	ax.plot(X, Y)

	for n in range (8):
		plotDiag(n*tau/8)
	#ax.set_title(r"Rotation around the $\frac{\pi}{4}$ axis")#
	return []
'''


#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''

if __name__=="__main__":
	global fig
	fig = plt.figure()
	fig.set_tight_layout(True)

	duration = 5
	fps = 25

	global ax
	ax = plt.subplot(111)
	ax.axis('off')

	'''
	xlimits = expandAxisLimit(0, tan(pi/8) )
	ylimits = expandAxisLimit(0,0.366) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)
	'''	
	ax.set_xlim([0,tan(pi/8)])
	ax.set_ylim([0,0.366])

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	#line, = ax.plot([0,0+0.01], [0,0+0.01] , color = 'r', marker = 'o')
	(line,) = ax.plot([0],[0], color = 'r', marker = 'o')

	BGIP()

	RotationMatrices = ReadR("Matrices/1FrameRotationMatrices.txt")
	#RotationMatrices2= ReadR("Matrices/128FrameRotationMatrices.txt")
	
	#curve = sphereFillingCurve(1, 6, duration, fps)
	X, Y = [], []

	def draw(f):
		'''
		[theta, theta_axis, phi_axis] = curve[f]
		x_axis, y_axis, z_axis = spherical_cartesian(pi/2, pi/4)
		s = sin(theta/2)
		q = [cos(theta/2), s*x_axis, s*y_axis, s*z_axis]
		print("converting quaternion of frame",f+1)
		R = QuatToR(q)
		'''
		v48 = R_v(RotationMatrices[f])

		r = chooseIPpoint(v48)

		[Theta, Phi] = cartesian_spherical(r[0],r[1],r[2])

		R, Angle = stereographicProjector(Theta,Phi)
		Xtemp, Ytemp = polar2D_xy(Angle, R)
		X.append(Xtemp)
		Y.append(Ytemp)
		#line.set_data([X],[Y])

		return (line,)
	for pic in range (8):
		draw(pic)
	line.set_data([X],[Y])
	line.set_linestyle("")
	#print(dir(line))
	saveName = "ForDavid/Frame1RotAll"+"_Ocean_s_code.png"#str(pic+1)+
	plt.savefig(saveName)

	#anim = animation.FuncAnimation(fig, draw, init_func = BG, frames = int(8), interval = 40, blit=True)
	#anim.save( 'Testanim.mp4', fps = 25, extra_args=['-vcodec', 'libx264'])
