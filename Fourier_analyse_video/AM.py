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

import numpy as np
import subprocess as sp
FFMPEG_BIN = "ffmpeg"
from PIL import Image

#0. Define variables
xdim = 1280
ydim = 720
fps = 25
nframe = 6642	#found by FFprobe
color = 3
num_pix = xdim*ydim 	#=number of pixels in one frame
run_time = nframe/fps	#=265.68 seconds
vid = "Arctic Monkeys - Do I Wanna Know- (Official Video).mp4"

def get_frames(m,s):	#input
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
	#3. Turn the byte read into a numpy array
	snippet = np.fromstring(pixels, dtype='uint8')
	snippet = snippet.reshape(fps, ydim, xdim, color)	#must divide it up this way, otherwise the computer will crash.
	#returns: snippet[no. of frame, array]	[y(up to down), array][x][color, arrays]
	#for the purpose of getting a vertical frame
	return snippet
	pipe.stdout.flush()

#Note to self: (tuple) [list]=[array]
#PIL Image only accept tuple

got_frame = get_frames(1, 38)
#get the 25th frame in arrays(y) of arrays(x) of arrays(color)
frame = [0]*25
#Debugging module here: (generates all frames in one second of the video)

'''
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
	print(len(frame[0]))
	print(type(frame[0]))
	print(len(frame[0][0]))
	print(type(frame[0][0]))
'''
