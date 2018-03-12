#!/home/oceanw/anaconda3/bin/python
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from scipy.interpolate.interpolate import interp1d
#This file does not contain reading functions, as it simply does the job of mathematical processing.



#General functions to switch coordinates.
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def polar2D_xy(Angle, R):
	return R*cos(Angle), R*sin(Angle)

def stereographicProjector(Theta, Phi):
	return tan(Theta/2), Phi

def spherical_cartesian(theta, phi):
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return [x,y,z]

def cartesian_spherical(x, y, z):
	x,y,z = np.array([x,y,z], dtype=float) #change the data type to the desired format

	Theta = arccos(z)
	Phi = arctan(np.divide(y,x))
	Phi = np.nan_to_num(Phi)
	Phi+= np.array( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return np.array([Theta, Phi])



#Plotters
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def expandAxisLimit(Min, Max, fraction=0.1):
	offSet = fraction*(Max-Min)
	return [Min-offSet, Max+offSet]

def Diag_xy(phi, r_lower=0, r_upper=1):
	return polar2D_xy([phi,]*2, [r_lower, r_upper])

def point_xy(x,y,z): #This function is created for convenience only.
	theta_an, phi_an = cartesian_spherical(x,y,z)
	R_an, Angle_an = stereographicProjector(theta_an, phi_an)
	x_an, y_an = polar2D_xy( Angle_an, R_an )
	return x_an, y_an

def DrawCircle( cTheta, cPhi, a = pi/2 ): # a is the angular radius
	t = np.linspace(0,tau,400)
	
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)

	return Theta, Phi

def drawHalfCircle(cTheta, cPhi, a = pi/2): # copy of the DrawCircle function above
	t = np.linspace( pi , pi+arccos(sqrt(2/3)),100)#But this one parametrically draws the RHS curve of the Inverse Pole Figure.
	#i.e. plot the greater circle at the axis normalize([ 0,-1, 1]), starting at the highest point 
	#(i.e. the point that is pi radians away from the bottom)
	#to the point that touches the corner, i.e. arccos(sqrt(2/3)) down from the highest point.
	#This corresponds to 1/2 of one of the top edge, from the centre to the side.
	#Find the x,y,z coordinate of the centre
	[x0, y0, z0] = spherical_cartesian(cTheta,cPhi)

	#Find the x,y,z coordinates of the point directly below it, from which the plotting will start.
	[xt, yt, zt] = spherical_cartesian( cTheta+pi/2,cPhi )

	x1 = x0*cos(a) + sin(a)*sin(t)*(y0*zt-z0*yt) + sin(a)*cos(t)*y0*(xt*y0-yt*x0) - sin(a)*cos(t)*z0*(zt*x0-xt*z0)
	y1 = y0*cos(a) + sin(a)*sin(t)*(z0*xt-x0*zt) + sin(a)*cos(t)*z0*(yt*z0-zt*y0) - sin(a)*cos(t)*x0*(xt*y0-yt*x0)
	z1 = z0*cos(a) + sin(a)*sin(t)*(x0*yt-y0*xt) + sin(a)*cos(t)*x0*(zt*x0-xt*z0) - sin(a)*cos(t)*y0*(yt*z0-zt*y0)

	[Theta,Phi] = cartesian_spherical(x1, y1, z1)
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	return R, Angle

def InversePoleFigureLine():
	R , Angle = drawHalfCircle( pi/4,pi )

	EdgeR = 0
	EdgeA = 0
	EdgeR = np.append(EdgeR, R)
	EdgeA = np.append(EdgeA, Angle)
	EdgeR = np.append(EdgeR, 0)
	EdgeA = np.append(EdgeA, pi/4)

	X,Y = polar2D_xy(EdgeA,EdgeR)
	return [X,Y]

def getIPtip():
	s3 = sqrt(1/3)
	theta_an, phi_an = cartesian_spherical(s3,s3,s3)
	R_an, Angle_an = stereographicProjector(theta_an, phi_an)
	x_an, y_an = polar2D_xy( Angle_an, R_an )
	return x_an,y_an

def getTaylorCurveDiv():
	xdata = [0.2464348739, 0.1295609244]
	y = [0.001275906, 0.1306574186]
	x = np.linspace(max(xdata), min(xdata),60)
	f = interp1d(xdata, y)
	y = f(x)
	return np.array([x,y])

def getTaylorCurve2():
	xdata = [0.2152941176, 0.1883823529, 0.158394958, 0.1276386555, 0.0930378151, 0.0561302521, 0.0007689076]
	y = [0.0008297794, 0.0274612132, 0.0502737395, 0.0524971639, 0.0417500788, 0.022610688, -0.0003796481]
	x = np.linspace(max(xdata), min(xdata),60)
	f = interp1d(xdata, y, kind = 'cubic')
	y = f(x)
	return np.array([x,y])

def getTaylorCurve3():
	xdata, ydata = [], []
	xdata.append([0.2967983193, 0.2691176471, 0.2429747899, 0.232210084, 0.2337478992, 0.249894958, 0.2775756303, 0.3091008403, 0.3437016807, 0.366])
	ydata.append([0.0017620798, 0.0299169118, 0.0626499475, 0.096177521, 0.1358307248, 0.1755143645, 0.2304720326, 0.2823877101, 0.3343097952, 0.36714375])

	xdata.append([0.2698865546, 0.2406680672, 0.2176008403, 0.1999159664, 0.1983781513, 0.2106806723, 0.2383613445, 0.2675798319, 0.3152521008, 0.3529285714, 0.3667689076])
	ydata.append([0.0017060137, 0.0329576418, 0.0572595851, 0.0915352416, 0.1250820378, 0.1571326681, 0.1998903361, 0.238076208, 0.2968880252, 0.3450040179, 0.3679078519])

	xdata.append([0.3560042017, 0.329092437, 0.3198655462, 0.3190966387, 0.3283235294, 0.3460084034, 0.3590798319, 0.366])
	ydata.append([0.0018854254, 0.0491043592, 0.0833976366, 0.1428710347, 0.2183777574, 0.2847521008, 0.337391833, 0.36714375])

	X, Y = [], []
	for n in range (len(xdata)):
		yi = np.linspace( min(ydata[n]), max(ydata[n]),60)
		Y.append(  yi )
		f = interp1d(ydata[n], xdata[n], kind = 'cubic')
		X.append(f(yi))
	return np.array([X,Y])


#Main functions
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def naturalNum(Index):
	if np.sign(Index)!=-1: return Index
	else: return 0

def normalize(r):
	return r/RootSumSq(r)

def deNormalize(v):
	return v/(2*abs(v[2]))

def R_v(R):
	Z = np.array([0,0,1]) #assume pulling axis is the z axis.
	[x,y,z] = np.linalg.multi_dot([R,Z]) #see where does the pulling axis lands.
	#Pick the vector that juts out of the top face:
	return duplicate48Points(x,y,z)

def duplicate48Points(x0,y0,z0): #Find the equivalent points by permuating the indices and adding negative signs.
	[x0,y0] = np.array([x0,y0])
	x,y,z = [], [], []
	
	for n in range (8):
		x.append((-1)**(n>>2) *x0); y.append((-1)**(n>>1) *y0); z.append((-1)**(n>>0) *z0)
		x.append((-1)**(n>>2) *y0); y.append((-1)**(n>>1) *x0); z.append((-1)**(n>>0) *z0)
		x.append((-1)**(n>>2) *x0); y.append((-1)**(n>>1) *z0); z.append((-1)**(n>>0) *y0)
		x.append((-1)**(n>>2) *y0); y.append((-1)**(n>>1) *z0); z.append((-1)**(n>>0) *x0)
		x.append((-1)**(n>>2) *z0); y.append((-1)**(n>>1) *x0); z.append((-1)**(n>>0) *y0)
		x.append((-1)**(n>>2) *z0); y.append((-1)**(n>>1) *y0); z.append((-1)**(n>>0) *x0)

	return np.array([x,y,z]).T

def chooseIPpoint(arrayOf48pt):
	for r in arrayOf48pt:
		if ( sum(np.sign(r)>-np.ones(3))==3# all components are non-negative.
			) and ( abs(r[0])>=abs(r[1])
			) and ( abs(r[0])<=abs(r[2])
			) and ( abs(r[1])<=abs(r[2]) ):
			return r

def getIPpointID(arrayOf48pt):
	for n in range (len(arrayOf48pt)):
		if ( sum(np.sign(arrayOf48pt[n])>-np.ones(3))==3# all components are non-negative.
			) and ( abs(arrayOf48pt[n][0])>=abs(arrayOf48pt[n][1])
			) and ( abs(arrayOf48pt[n][0])<=abs(arrayOf48pt[n][2])
			) and ( abs(arrayOf48pt[n][1])<=abs(arrayOf48pt[n][2]) ):
			return n

def choosePFpoint(arrayOf48pt):
	pointList = []
	n = 0
	while len(pointList)<24:
		r = arrayOf48pt[n]
		if ( np.sign(r[2])>-1): #z is non-zero
			pointList.append(r)
		n += 1
	return pointList



'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#File reading functions
def ReadR(fileName):
	f = open( str(fileName) )
	Matrices = f.readlines()
	f.close()
	Matrices = np.reshape(Matrices, [-1,3])
	Matrix = []
	for n in range (len(Matrices)):
		Matrix.append(	[np.array(Matrices[n][0].split() , dtype=float),
				np.array( Matrices[n][1].split() , dtype=float),
				np.array( Matrices[n][2].split() , dtype=float) ] )
	#np.shape(Matrix) ==(n,3,3)
	return Matrix

def Readrho(fileName):
	f = open( str(fileName))
	rho = f.readlines()
	rho = np.array(rho, dtype = float)
	return rho



#Generators
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#sphereFillingCurve
def sphereFillingCurve( m,n , duration, fps=25):
	r = np.linspace(0,1,duration*fps)
	theta= sin(r) *pi
	phi = r*n*tau
	r = r*tau
	return np.array([r, theta, phi], dtype=float).T
