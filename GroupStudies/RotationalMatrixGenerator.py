#!/home/oceanw/anaconda3/bin/python
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
		theta=float(input("theta="))
		THETA=float(input("THETA="))
		PHI = float(input("PHI  ="))
		f.write(writeR(theta, THETA, PHI))
	f.close()
