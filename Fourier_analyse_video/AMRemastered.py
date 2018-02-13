#!/home/oceanw/anaconda3/bin/python3
#The audio stuff can be done on a separate file, and then digitally combined with a different python script.
#Optimization rule: comparison == minusing.
import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import quad as inte	#takes very little time to import 
from math import floor
from math import ceil
from scipy.interpolate import spline
from Debugging import save_1_second

#2:13 - 2:43 requires special treatment by having differnt y-offset or extracting vertical lines intead.



#declare variables____________________________________________________________________________________________________________________________
xdim    = 1280
ydim    = 720
fps     = 25
nFrame  = 6642	#number of frames in this video, found by FFprobe
color   = 3
#outColor=5
num_pix = xdim*ydim 	#=number of pixels in one frame
run_time= nFrame/fps	#=265.68 seconds
yoffset = -0.25 + ydim/2	
vid     = "Arctic Monkeys - Do I Wanna Know- (Official Video).mp4"
nCo     = 60	#number of coefficient in fourier analysis
specVal = 251
thresold= 0.1 #if more than thresold*100% of c-colored line is missing, then it is considered invalid as a line.
xThres  = thresold * xdim
yThres  = thresold * ydim



#declare classes______________________________________________________________________________________________________________________________
def mono_framexyIn_analogueOut(mono_framexy):
	return mono_framexy>>7
#This program is so short I could've merged it into the function; but for clarity I'll keep it.

class FRAME:
	def __init__(self, frame_cxy): #frame_yx [color][y][x].		#Schematic diagram:
		self.red   = mono_framexyIn_analogueOut( frame_cxy[0] )	#intermediate colors
		self.green = mono_framexyIn_analogueOut( frame_cxy[1] )	#intermediate colors
		self.blue  = mono_framexyIn_analogueOut( frame_cxy[2] )	#intermediate colors
		self.yellow= self.green  * self.red			#intermediate colors
		self.white = self.yellow * self.blue			#white	oooooo
		self.blue  = self.blue   - self.white			#blue	----oo
		self.green = self.green  - self.yellow			#green	--oo--
		self.red   = self.red    - self.yellow			#red	oo----
		self.yellow= self.yellow - self.white			#yellow	oooo--
			#type(bool).color[x][y]
class LINE:
	red, green, blue, yellow, white = [],[],[],[],[]

class existFlag:
	red, green, blue, yellow, white = True, True, True, True, True




#Declare subprograms for extraction:__________________________________________________________________________________________________________
def get_frames(m1, s1, d):	#input time, get one second worth of frames
	FFMPEG_BIN = "ffmpeg"
	#1. convert time
	if int(s1)==0:
		s1 = '59'
		m1 = str(int(m1)-1)
	else: s1 = str( (int(s1)-1) ).zfill(2)
	no_frame = int(d*fps)
	d = str(d)

	#2. Open the video as a subprocess
	command = [ FFMPEG_BIN, '-i', vid, '-t', d, '-f', 'image2pipe', '-pix_fmt', 'rgb24', '-vcodec', 'rawvideo', '-']
	pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=1000)
	#Take in the command list's arguments, use the standard stream, and open a buffer of size 1000

	#3. Read the required snippet, and reshape.
	snippet = np.fromstring( pipe.stdout.read(no_frame*ydim*xdim*color) , dtype='uint8' )
	
	pipe.stdout.flush()	#3. Close the program
	pipe.stdout.close()
	
	#snippet = np.fromstring(pixels, dtype='uint8') #This line should be deleted.
	snippet = snippet.reshape(no_frame, ydim, xdim, color)	
	#must divide it up this way, otherwise the computer will crash.

	return snippet #[no. of frames][y(up to down)][x(l to r)][color]

#Declare Subprograms for frame manipulation___________________________________________________________________________________________________
def meanInd(vertical_column): #can also be applied on horizontal_rows
	meanIndex = sum (np.arange(len(vertical_column)) * vertical_column) /np.sum(vertical_column)
	#BRUUUUTal one liner!
	return meanIndex

def numLines(vertical_column):
	np.sum( np.abs( np.diff(vertical_column) ) )/2  #+0.5 for every change
	return numLines

def scaleShiftLine(line):	#may need to scale the line by a factor of 255...
	return yoffset-np.array(line)

#for frame in Frames:
def multicolor_frameIn_multicolorLineOut(frame_yxc):
	#inheriting the parent's properties :)
	frame = FRAME( frame_yxc.T )
	lines = LINE()
	flag = existFlag()
	
	for c in ('red','green','blue','yellow','white'):
		framec = getattr( frame,c )
		
		if np.sum( framec )==0:	#Case of no such colour at all:
			setattr( flag,c , False )
		
		else: #case of having such colour:
			for xcoord in range (xdim):
				framecx = framec[xcoord]

				#case of 2+ lines detected:
				if ( numLines(framecx)>2 ): setattr( flag,c , False )
				
				else:		#case of 2 or 1 lines (acceptable):
					if np.sum(framecx)>0:
						setattr( lines,c , getattr(lines,c).append(meanInd(framecx)) )
					else:	#case of missing line:
						setattr( lines,c , getattr(lines,c).append( specVal ) )#append a special value instead

			#for the whole line:
			linec = np.ndarray.tolist( getattr( lines,c ) )
			if linec.count(specVal)<xThres:
				pass#for#*every instace of specVal, interpolate between the nearst two values, or nearest one value if n/a.
			else: setattr( flag,c , False)
		if getattr( flag,c )==True :setattr( lines,c , linec )
		else: setattr( lines,c , [] ); print("line",c,"is now set to an empty list")
	return (lines, flag)
	#Check for discontinuity: if more than two per xcoord, then that colour's line shouldn't be established.

#Subprogram for Fourier transform_____________________________________________________________________________________________________________
'''
def lineIn_FTGraphOut(W):
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
'''
def lineIn_FastFTGraphOut(line):
	line_raw = np.real(np.fft.rfft(line))/1000
	line_raw = np.split(line_raw, [nCo/2, len(line_raw)])[0]
	k = np.arange(nCo/2)
	return line_raw

def smoothen(y_values):
	a = len(y_values)
	new_x_axis = np.linspace(0, a, a*10)
	old_x_axis = np.linspace(0, a, a)
	b_smooth = spline(old_x_axis, y_values, new_x_axis)
	return (new_x_axis, b_smooth)


#Subprogram for plotting______________________________________________________________________________________________________________________
def preparePlot():
	fig = plt.figure()
	ax = plt.axes(xlim=(0, nCo), ylim=(-100,100))	#for lineIn_FTGraphOut: nCo, 2.
	ax.set_axis_bgcolor((0, 0, 0))			#for lineIn_FTGraphOut: nCo; FFT:nCo/2, as x upper bound.

	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	fig.set_tight_layout(True)
	#x.axis('tight')
	#plt.axis('off')
	line, = ax.plot([], [], lw=3, color = 'w')	#set the line style.
	return fig, (line,)

def init():
	line.set_data([], [])
	return line,

#Main Controller program______________________________________________________________________________________________________________________
def frame2smline(i):
	lines = multicolor_frameIn_multicolorLineOut(Frame[i])
	FTgraphs = lineIn_fastFTGraphOut(lines)
	(k, smoothlines) = smoothen(FTgraphs) #*Iterate for each color!
	line.set_data(k, smoothlines)
	return (line,)

def main():
	minute = str( input( "minute?" ) ).zfill(2)
	second = str( input( "second?" ) ).zfill(2)
	duration=float(input("duration?"))
	Frames = get_frames(minute, second, duration)

	#outputs boolean array with max index [numFrame][ydim][xdim][color]
	fig, (line,) = preparePlot()

	anim = animation.FuncAnimation(fig, frame2smline, init_func= init, frames = int(fps*duration), interval = 40, blit= True)
	anim.save( minute+'_'+second+'_dur='+str(duration)+'.mp4', fps = 25, extra_args=['-vcodec', 'libx264'])

if __name__=='__main__': main()
