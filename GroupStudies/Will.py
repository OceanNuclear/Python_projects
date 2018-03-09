#!/home/oceanw/anaconda3/bin/python
from math import sqrt
import numpy as np
def RotToQuat(R):  #R is the rotation matrix
	if( ((R[0][0] + R[1][1] + R[2][2]-1))<1E-10 ):
		s = sqrt(1 + R[0][0] + R[1][1] + R[2][2])*2	#s=4*w
		w = 0.25 * s
		x = ( R[2][1] - R[1][2] ) /s
		y = ( R[0][2] - R[2][0] ) /s
		z = ( R[1][0] - R[0][1] ) /s
 
	elif((R[0][0] > R[1][1])and(R[0][0] > R[2][2])): # rotational axis lies on 
		s = sqrt( 1.0 + R[0][0] - R[1][1] - R[2][2] )*2	#s=4*x
		w = (R[2][1] - R[1][2]) /s
		x = 0.25 * s
		y = (R[0][1] + R[1][0]) /s
		z = (R[0][2] + R[2][0]) /s
	  
	elif(R[1][1] > R[2][2]):
		s = sqrt( 1.0 + R[1][1] - R[0][0] - R[2][2] )*2	#s=4*y
		w = (R[0][2] - R[2][0]) /s
		x = (R[0][1] + R[1][0]) /s
		y = 0.25 * s
		z = (R[1][2] + R[2][1]) /s
 
	else:
		s = sqrt( 1.0 + R[2][2] - R[0][0] - R[1][1] )*2	#s=4*z
		w = (R[1][0] - R[0][1]) /s
		x = (R[0][2] + R[2][0]) /s
		y = (R[1][2] + R[2][1]) /s
		z = 0.25 * s
	Q = [w,x,y,z]	#identity matrix equates to [1,0,0,0]
	return Q

if __name__=='__main__':
	R = input("Rotation matrix?")
	R = [[1,0,0],[0,1,0],[0,0,1]]
	R = []
	R = np.array(R)
	print(RotToQuat(R))
