#!/home/oceanw/anaconda3/bin/python
#Write a short file consisting of rotation matrices with user defined ThreeVar (ThreeVar==[theta, THETA,PHI])
#This duplicate in the directory of Python_testing/QuaternionPaper is meant for generating matrix pairs for David to use on 12/06/18
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from generalLibrary import *
debug = False
normal= not debug



if __name__=="__main__":
	f= open((input("What's the file name?")+".txt"), 'w')
	for loopTime in range (7):
		theta=np.rad2deg(float(input("theta=")))
		THETA=np.rad2deg(float(input("THETA=")))
		PHI = np.rad2deg(float(input("PHI  =")))
		f.write(writeR(theta, THETA, PHI))
	f.close()
