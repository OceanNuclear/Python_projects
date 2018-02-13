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

