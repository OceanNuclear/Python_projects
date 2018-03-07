#!/home/oceanw/anaconda3/bin/python3
import numpy as np
from PIL import Image

def save_1_second(snippet):
	#expected input is frame = [[[[]*color]*xdim]*ydim]*fps
	for i in range (0,1):	#Saving only 1 frame here:
		#Here the intermediate frame evolves from a single, ordered frame, into a single linear frame.
		intermediate_frame = snippet[0]
		intermediate_frame = np.reshape(intermediate_frame, (num_pix, color))
		#linear frame is the tuple version of intermediate frame
		linear_frame = tuple(map(tuple, intermediate_frame))
		
		still = Image.new('RGB', (xdim,ydim))
		still.putdata(linear_frame)
		still.save('still_s=2'+str(i)+'.jpg', 'JPEG')
#Decommissioned subprograms

def checkshape( a , Shape ):
	if np.shape(a)==Shape: return
	else: raise ValueError

def save_mono_frame(monoframe):
	checkshape(monoframe, [1280,720])
	#*img = Image.load(monoframe)
	img.save(monoframe , color = 'greyscae')
	return
'''

def meanInd(vertical_column): #can also be applied on horizontal_rows
	indices = np.arange(len(vertical_column)) #expect a boolean input, and here's their indices.
	mean = (np.sum (indices*vertical_column) / np.sum(vertical_column) ) #Sum/weight-factor
	#*mean = np.nonzero( 
	return mean

def numLines(vertical_column):
	return np.sum( np.abs( np.diff(vertical_column) ) )/2

class existFlag:
	red, green, blue, yellow, white = True, True, True, True, True
'''
