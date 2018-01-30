#!/home/oceanw/anaconda3/bin/python

import test2 as t2
import numpy as np
import scipy as sp
import os

global someVar
someVar = input("type something for the computer to spit back at you:")

def printer(userInput):
	addOne(userInput)
	global x;	print(x)
	x = 1
	print(Integer)
	print (x)

def addOne(anyInput):
	global Integer
	Integer = int(anyInput)+1
	#global Integer

x = 1;
printer(someVar)
t2.dummy(x)

def loop1():
	loop1()
	loop2()
def loop2():
	print("This is loop 2")
	loop1()

#print(x)

#Global variable from a header file can be imported as h.globvar
#The order at which the subprograms are arranged, relative to each other, doesn't matter.
#BUT they must come BEFORE the main body of the program. 
#Also numpy should've been imported in the header file individually.
#Subprogram are able to use variables (and their assigned values) declared before they were called, in the body of __main__.

	#If you write assign a value to the vairable, and then push this variable into global, then it'll give a warning, but it'll work fine. Not recommended though.
	#Self-referencing loops autoterminates, as it reaches a maximum recursion depth. Bedrock, if you would.
