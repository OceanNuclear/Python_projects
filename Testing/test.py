#!/home/oceanw/anaconda3/bin/python

import test2 as t2
import numpy as np
import scipy as sp
import os

global someVar
someVar = input("type something for the computer to spit back at you:")

def printer(userInput):
	addOne(userInput)
	print(Integer)

def addOne(anyInput):
	global Integer
	Integer = int(anyInput)+1
	#global Integer
x = 1
printer(someVar)
t2.dummy(x)
#print(x)

#So the ORDER at which the subprograms are arranged doesn't matter.
#As long as they are active (not commented out), it's fine.
#Be careful that when you declare a variable in your header file as global you may risk sharing it with the __main__.
#If you write assign a value to the vairable, and then push this variable into global, then it'll give a warning, but it'll work fine.
#Why though?

