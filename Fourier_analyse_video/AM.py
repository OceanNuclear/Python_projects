#!/home/oceanw/anaconda3/bin/python3
#A project intended to fourier analyse the waves on a video.
#OpenCV is not usable on Linux due to conflict issues.
#So instead I will be using FFmpeg as a subprocess (pipe) to approach this problem.

#Segments to be fourier analysed:
#00:00-01:13 (W)
#01:13-01:26 (W-B)
#01:26-01:35 (W)
#01:35-01:36 (W)
#02:00-02:11 (W-Y-B-G-R)
#02:13-02:14 (vertical, W-Y-B)
#02:17-02:21 (W-G-R)
#02:21-02:28 (WRBY horizontal decending)
#02:32-02:41 (WRBY vertical left-to-right)
#02:46-02:49 (W)
#02:51-02:54 (W)
#02:56-02:59 (W)
#04:20-04:21 (W)

#Newest commit: split the whole code into more usable modules.

'''
Next steps:
Separate out these as modules:
	Filtering
	(NOT fourier analysis! Not worth the time)
Modify the seeking function to be more precise
publish it as an animation of the size of xdim/2 x ydim/2
publish a one second clip of it
Add a filter that collect the colored lines
interpolate the colored lines, then print it out
Add in the colored lines' k space plot
Animate each of the above segments
String together these segments
Add in black screen at appropriate times, and then publish
shrink the original to half size and put it right next to the video.
Publish with the original audio.


**find an audio module
**fourier transform the audio too, cause why not
add in the last two at the bottom
'''

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
#The more niche dependencies are put inside the subprograms

#0. Define variables
xdim = 1280
ydim = 720
fps = 25
nframe = 6642	#number of frames in this video, found by FFprobe
color = 3
num_pix = xdim*ydim 	#=number of pixels in one frame
run_time = nframe/fps	#=265.68 seconds
yoffset = ydim/2		#to counter the 
vid = "Arctic Monkeys - Do I Wanna Know- (Official Video).mp4"
nCo = 60	#number of coefficient in fourier analysis


#0. Subprogram for fetching snippets of the video
def get_frames(m,s):	#input time, get one second worth of frames
	import subprocess as sp
	FFMPEG_BIN = "ffmpeg"
	#0. convert time
	if (s==0): s = 59
	else: s = str(s-1).zfill(2)
	time = '00:0'+str(m)+':'+str(s)
	#1. Open the video as a subprocess
	command = [ FFMPEG_BIN,
		'-ss', time,	#skip to t-1
		'-i', vid,
		'-ss', '1',
		'-t', '1',
		'-f', 'image2pipe',
		'-pix_fmt', 'rgb24',
		'-vcodec', 'rawvideo', '-']
	pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=1000)

	#2. Read one second of the frame
	pixels = pipe.stdout.read(color*ydim*xdim*fps)
	pipe.stdout.flush()
	#3. Turn the byte read into a numpy array
	snippet = np.fromstring(pixels, dtype='uint8')
	snippet = snippet.reshape(fps, ydim, xdim, color)	#must divide it up this way, otherwise the computer will crash.
	#returns: snippet[no. of frame, array]	[y(up to down), array][x][color, arrays]
	#for the purpose of getting a vertical frame

	return snippet



def frame2line1(frame):
	W = [0]*xdim
	WT= [0]*xdim
	for x in range (0,xdim):
		for y in range (0, ydim):
			if (frame[0][x][y]>10) or (frame[1][x][y]>10) or (frame[2][x][y]>10): #if this pixel has any color at all
				W[x] += yoffset-y
				WT[x] +=1
		W[x]= W[x]/WT[x]
	return(W)


def line2fouriergraph(W):
	from math import floor
	from math import ceil
	B = [0] * nCo	#note that the 0-th coefficient is used for cos instead of sine.
	Y = [0] * nCo	#the product function to be integrated in the n-th harmonic.
	import scipy.integrate as inte
	Y[0] = lambda x : ((W[int(ceil(x))])*(x-floor(x))+W[int(floor(x))]*(ceil(x)-x))
	B[0] = (2/xdim)*inte.quad(Y[0], 0, xdim-1)[0]

	for n in range (0, nCo):
		Y[n] = lambda x : np.sin(n*np.pi*x/xdim)*((W[int(ceil(x))])*(x-floor(x))+W[int(floor(x))]*(ceil(x)-x))
		#the ceil and floor function are here to interpolate
		B[n] += (2/xdim)*inte.quad(Y[n], 0, xdim-1)[0]
		#Aesthetic: smooth out the line
	return(B)


def smoothen(y_values):
	from scipy.interpolate import spline
	a = len(y_values)
	new_x_axis = np.linspace(0, a, a*10)
	old_x_axis = np.linspace(0, a, a)
	b_smooth = spline(old_x_axis, y_values, new_x_axis)
	return (new_x_axis, b_smooth)


def plotbg():
	ax = plt.axes(xlim=(0, nCo), ylim=(-60,60))
	ax.set_axis_bgcolor((0, 0, 0))

def plot(x, y, c):
	plt.setp(plt.plot(x, y), color = c, linewidth = 3.0 )


def White(t1, t2):
	#6th second,
	got_frame = get_frames(0, 6)#get the frames in arrays(y) of arrays(x) of arrays(color)
	
	#1. For the 0-th frame:
	frame = np.transpose(got_frame[0])
	#the format is frame[color][xdim][ydim]
	White_line = frame2line1(frame)
	
	White_B_raw = line2fouriergraph(White_line)
	
	(k, WB) = smoothen(White_B_raw)
	
	plotbg()
	plot(k, WB, 'w')
	#plot(x, z, 'b')
	#plot(x, w, 'r')
	plt.show()

	return

White(1, 1)
	
#Underconstruction:
'''
def Anim

def frame_no2time(no):


def time2frame_no(m, s):
	s += 60*m
	s*fps
'''	

#Debugging modules are here: (generates all frames in one second of the video)
'''
#geneating test functions
def generate_test_function():
	x = np.linspace(0, nCo, nCo*10)
	y = x
	z = y/2
	w = -y
'''


'''
#2. re-construct the graph using the data.(optional)
def plot2(x, W):
	x = W-W
	plt.plot(x, W)
	plt.show()
'''


'''
#Note to self: (tuple) [list]=[array]
#PIL Image only accept tuple
def save_1_second():
	frame = [0]*25
	for i in range (0,1):
		frame[i] = got_frame[i]
		frame[i] = np.reshape(frame[i], (num_pix, color))
		frame[i] = tuple(map(tuple, frame[i]))
	
		still = Image.new('RGB', (xdim,ydim))
		still.putdata(frame[i])
		still.save('still_00:59_'+str(i)+'.jpg', 'JPEG')
'''


'''
#And this is for debugging the debugging code :)
def printing(frame)
	print(np.shape(frame))
	print(type(frame))	
	print(np.shape(frame[0]))
	print(type(frame[0]))
	print(np.shape(frame[0][0]))
	print(type(frame[0][0]))
'''
