#!/home/oceanw/anaconda3/bin/python
import numpy as np
from numpy import pi
from quat import *
tau = pi*2
from generalLibrary import *



def FileReader(frame):
	prepender=""
	appender="FrameRotationMatrices.txt"
	folder="NewModel/"
	f = open(folder+prepender+str(frame)+appender)
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

if __name__=="__main__":
	while True:
		frame = int(input("What is the frame number where discontinuity occurred?"))
		grain = int(input("Which grain is the culprit?"))
		print("Before discontinuity, the Rotation Matrix is")
		R = FileReader(frame-1)
		q = RotToQuat(R[grain])
		[theta,axis]=QuatToRotation(q)
		print("\t i.e. in polar coordinates,")
		print("\t angle of rotation [theta phi]=")
		print("\t",np.rad2deg(theta),np.rad2deg(cartesian_spherical(axis[0],axis[1],axis[2])),"degrees")
		r = chooseIPpoint( R_v(R[grain]) )
		print("\t The vector that will be plotted on the pole figure is",deNormalize(r))
		[theta_graph, phi_graph] = cartesian_spherical(r[0],r[1],r[2])
		R_graph, Angle_graph = stereographicProjector(theta_graph, phi_graph)
		print("\t which is then projected onto R=",R_graph,"Angle=",np.rad2deg(Angle_graph),"degrees.")

		print("After discontinuity, the Rotation Matrix is")
		R = FileReader(frame)
		q = RotToQuat(R[grain])
		[theta,axis]=QuatToRotation(q)
		print("\t i.e. in polar coordinates,")
		print("\t angle of rotation, [theta, phi]=")
		print("\t",np.rad2deg(theta),np.rad2deg(cartesian_spherical(axis[0],axis[1],axis[2])),"degrees")
		r = chooseIPpoint( R_v(R[grain]) )
		print("\t The vector that will be plotted on the pole figure is",deNormalize(r))
		[theta_graph, phi_graph] = cartesian_spherical(r[0],r[1],r[2])
		R_graph, Angle_graph = stereographicProjector(theta_graph, phi_graph)
		print("\t which is then projected onto R=",R_graph,"Angle=",np.rad2deg(Angle_graph),"degrees.")
		print("\n")
