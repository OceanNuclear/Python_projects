#!/home/oceanw/anaconda3/bin/python3
#A project intended to fourier analyse the waves on a video.
#Why? 
#...
#Because I can.
#A project by Ocean Wong, throughout May of 2017.
#Nuclear Science and Materials student at UoB.

#OpenCV is not usable on Linux due to conflict issues.
#So instead I will be using FFmpeg as a subprocess (pipe) to approach this problem.

#Segments to be fourier analysed:
#00:00-01:13 (W)/
#01:13-01:26 (W-B)
#01:26-01:35 (W)/
#01:35-01:36 (W)/
#02:00-02:11 (W-Y-B-G-R)
#02:13-02:14 (vertical, W-Y-B)
#02:17-02:21 (W-G-R)
#02:21-02:28 (WRBY horizontal decending)
#02:32-02:41 (WRBY vertical left-to-right)
#02:46-02:49 (W)/
#02:51-02:54 (W)/
#02:56-02:59 (W)/
#04:20-04:21 (W)/

'''
Next steps:
Separate out these as modules:
1. Filtering, needs optimization by analogizing?
	SUCCESSFUL. Time on this step per frame is now 0.5s.
2. Modify the seeking function to be more precise, and run for longer.
	SUCCESSFUL.
2.4: Create a separate subprogram(White_line_plot ?) to plot the white line: NOT NECESSARY
2.5: Replace the subprocess with direct ffmpy retrieval of the video?
	#ffmpy.readthedocs.io/en/latest/examples.html#using-pipe-protocol
	Apparently ffmpy is just the the subprocess below.
	There's no performance benefit by carrying out this step.
3. Make an animation module: SUCCESSFUL
	ATM I have fourier analysed the first snippet.
3.5: Adjust size so that the area will be 640x360?
	Nah, that can wait.
3.55: Now I need to redo most of the first segment with the new-found yoffset.
3.6: Find the number of black frames at the start of the video, set this number to x, output a video of corresponding number of frames at 25 fps. 
	Can duplicate this very code, modfiy the s float(input) instead of int(input), then start the fourier analysis at x+1 frame.
4. publish the first 73s as an animation (of the size of xdim/2 x ydim/2?)
	Published as 2 second clips.
5. Add a filter that collect the colored lines
6. interpolate the colored lines, then print it out
7. Add in the colored lines' k space plot
8. Animate each of the above segments
9. String together these segments
10.Add in black screen at appropriate times, and then publish
11.shrink the original to half size and put it right next to the video.
12.Publish with the original audio.


**Make an audio module
https://stackoverflow.com/questions/9913032/ffmpeg-to-extract-audio-from-video
**fourier transform the audio too, because why not
add in the last two at the bottom
Fourier analysis step can be optimized by replacing integration with FFT; but I chose not to because that has lower resolution.
'''
#saving each frame takes 1.5s!

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import quad as inte
from math import floor
from math import ceil


#0. Define variables
xdim = 1280
ydim = 720
fps = 25
nframe = 6642	#number of frames in this video, found by FFprobe
color = 3
num_pix = xdim*ydim 	#=number of pixels in one frame
run_time = nframe/fps	#=265.68 seconds
yoffset = -0.25 + ydim/2	
vid = "Arctic Monkeys - Do I Wanna Know- (Official Video).mp4"
nCo = 60	#number of coefficient in fourier analysis
Red = 0
Green=1
Blue= 2

#Subprogram for fetching snippets of the video
#1
def get_frames(m1, s1, d):	#input time, get one second worth of frames
	import subprocess as sp
	FFMPEG_BIN = "ffmpeg"
	#0. convert time
	if (s1==0): s1 = 59
	else: s1 = str(s1-1).zfill(2)
	time_s = '00:0'+str(m1)+':'+str(s1)
	no_frame = int(d*fps)
	d = str(d)
	#1. Open the video as a subprocess
	command = [ FFMPEG_BIN,
		'-i', vid,
		'-t', d,
		'-f', 'image2pipe',
		'-pix_fmt', 'rgb24',
		'-vcodec', 'rawvideo', '-']
	pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=1000)
	#Take in the command list's arguments, use the standard stream, and open a buffer of size 1000

	#2. Read one second of the frame
	pixels = pipe.stdout.read(no_frame*ydim*xdim*color)
	
	#3. Close the program
	pipe.stdout.flush()
	pipe.stdout.close()

	#4. Turn the byte read into a numpy array
	snippet = np.fromstring(pixels, dtype='uint8')
	snippet = snippet.reshape(no_frame, ydim, xdim, color)	
	#must divide it up this way, otherwise the computer will crash.
	#returns: snippet[no. of frame, array][y(up to down), array][x, array][color, arrays]
	#for the purpose of getting a vertical frame
	return snippet
#Outside of this subprocess all data are ordered in ([fps])[y][x][color]


#2
def analogize(snippet):
	snippet = snippet>>7
	snippet = snippet*255	#now we have 25 frames of image with analogue pixel values
	return snippet



#White line
#2
def analogueframe2line1(frame):#input frame, output line
	uframe = np.transpose(frame)#we want to deal with color first instead [color][x][y]
	W = [0]*xdim
	WT= [0]*xdim
	for x in range (1, xdim):
		WT[x] = np.sum(uframe[Red][x])/255
		sortedset = np.argsort(uframe[Red][x])
		#Used this argsort step to replace the if-conditions
		sortedset = np.split(sortedset, [int(ydim-WT[x]),ydim])[1]
		W[x] = yoffset-np.mean(sortedset)
	return(W)

'''
#White line
def analogueframe2line1(frame):#input frame, output line
	uframe = np.transpose(frame)#we want to deal with color first instead [color][x][y]
	W = [0]*xdim
	WT= [0]*xdim
	for x in range (1, xdim):
		lowerlimit = int(yoffset-W[x-1]-100)
		for y in range (lowerlimit, lowerlimit+200):
			#Each full-frame calculation/or-condition takes an extra 10 seconds,
			#So I'm instead takinge advantage of the continuity of the function.
			if (uframe[0][x][y]>10) and (uframe[1][x][y]>10) and (uframe[2][x][y]>10):
				W[x] += yoffset-y
				WT[x] +=1
		W[x]= W[x]/WT[x]
	return(W)
'''


#White+blue lines
#3
def frame2line2(frame):#input frame, output lines
	uframe = np.transpose(frame)#we want to deal with color first instead
	W = [0]*xdim
	WT= [0]*xdim
	B = [0]*xdim
	BT= [0]*xdim
	for x in range (0,xdim):
		for y in range (0, ydim):
			#Each full-frame calculation/or-condition takes an extra 10 seconds.
			if (uframe[Blue][x][y]>10): 
				if(uframe[Red][x][y]<10):
					W[x] += yoffset-y
					WT[x]+=1
				else:
					B[x] += yoffset-y
					BT[x]+=1
		W[x]= W[x]/WT[x]
		B[x]= B[x]/BT[x]
	return(W,B)


#4
def line2fouriergraph1(W):
	B = [0] * nCo	#note that the 0-th coefficient is used for cos instead of sine.
	Y = [0] * nCo	#the product function to be integrated in the n-th harmonic.
	Y[0] = lambda x : ((W[int(ceil(x))])*(x-floor(x))+W[int(floor(x))]*(ceil(x)-x))
	B[0] = (2/xdim)*inte(Y[0], 0, xdim-1)[0]
	for n in range (1, nCo):
		Y[n] = lambda x : np.sin(n*np.pi*x/xdim)*((W[int(ceil(x))])*(x-floor(x))+W[int(floor(x))]*(ceil(x)-x))
		#the ceil and floor function are here to interpolate
		B[n] += (2/xdim)*inte(Y[n], 0, xdim-1)[0]
		#Aesthetic: smooth out the line
	return(B)

#5
#Fast fourier transform
def line2fouriergraph2(line):
	line_raw = np.real(np.fft.rfft(line))/1000
	line_raw = np.split(line_raw, [nCo/2, len(line_raw)])[0]
	k = np.arange(nCo/2)
	return line_raw


#6
def smoothen(y_values):
	from scipy.interpolate import spline
	a = len(y_values)
	new_x_axis = np.linspace(0, a, a*10)
	old_x_axis = np.linspace(0, a, a)
	b_smooth = spline(old_x_axis, y_values, new_x_axis)
	return (new_x_axis, b_smooth)


#6: assimilated module for setting bg color

#7
def plot(x, y, c):
	plt.setp(ax.plot(x, y), color = c, linewidth = 3.0 )

#8
'''
def MainWB(t1, t2):
	#6th second,
	snippet = get_frames(0, 10, 1.04)#snippet = a snippet of 1 second. [fps][ydim][xdim][color]
	
	#1. For the 0-th frame:
	(White_line, Blue_line) = frame2line2(frame[27])
	
	White_line= interpolate(White_line)
	Blue_line = interpolate(Blue_line)

	White_B_raw= line2fouriergraph1(White_line)
	Blue_B_raw = line2fouriergraph1(Blue_line)

	(k, WB) = smoothen(White_B_raw)
	(k, BB) = smoothen(Blue_B_raw)

	plotbg()
	plot(k, WB, 'w')
	#plot(k, z, 'b')
	#plot(x, w, 'r')
	plt.show()
'''
#^v Commented away to stop myself from changing the wrong program

'''
def Anim

def frame_no2time(no):


def time2frame_no(m, s):
	s += 60*m
	return (int(s*fps))
'''	

#Debugging modules are here: (generates all frames in one second of the video)_________________________________________________________________________


#geneating test functions
#9
def Just_plot_White_line(frame):#input frame, output plot of line in the frame
	White_line = analogueframe2line1(frame)
	x = np.arange(len(White_line))
	plt.plot(x,White_line)
	plt.show()



#10
def generate_test_function():
	x = np.linspace(0, nCo, nCo*10)
	y = x
	z = y/2
	w = -y



#2. re-construct the graph using the data.(optional)
#11
def plot2(W):
	x = np.arange(len(W))
	plt.plot(x, W)
	plt.show()
#_________________________________________________________________________Hi the main program's line is currently stored here.______________


#Note to self: (tuple) [list]=[array]
#PIL Image only accept tuple
#Outside of this image processing subprogram all data are ordered in ([fps])[y][x][color]
#12
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
#And this is for debugging the debugging code :)
#13
def printing(frame):
	print(np.shape(frame))
	print(type(frame))	
	print(np.shape(frame[0]))
	print(type(frame[0]))
	print(np.shape(frame[0][0]))
	print(type(frame[0][0]))
'''____________________________________________________________________________________________________________________________________________________
____________________________________________________________________________________________________________________________________________________'''
m = int(input("minute? "))
s = int(input("second? "))
d = float(input("length to be analyse? "))

fig = plt.figure()
ax = plt.axes(xlim=(0, nCo), ylim=(-100,100))	#for line2fouriergraph1: nCo, 2.
ax.set_axis_bgcolor((0, 0, 0))			#for line2fouriergraph1: nCo; FFT:nCo/2, as x upper bound.

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
fig.set_tight_layout(True)
#x.axis('tight')
#plt.axis('off')
line, = ax.plot([], [], lw=3, color = 'w')	#set the line color and stuff.


def init():
	line.set_data([], [])
	return line,


def frame2smline(i):
	#1. For the 0-th frame:
	White_line = analogueframe2line1(snippet[i])
	#White_B_raw = line2fouriergraph1(White_line)
	White_B_raw = line2fouriergraph1(White_line)
	(k, WB) = smoothen(White_B_raw)
	line.set_data(k, WB)
	return line,

snippet = get_frames(m, s, d)#snippet = a snippet of 1 second. [fps][ydim][xdim][color]
snippet = analogize(snippet)
anim = animation.FuncAnimation(fig, frame2smline, init_func= init,
                               frames = int(fps*d), interval = 40, blit= True)

#saving the animation
s = str(s).zfill(2)
m = str(m).zfill(2)
d = str(d)
anim.save(m+'_'+s+'_dur='+d+'.mp4', fps = 25, extra_args=['-vcodec', 'libx264'])
