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



'''#declare variables███████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
#Colours!
color	= 3
cList   = ('red','green','blue','yellow','white')
outColor= len(cList)
R,G,B,Y,W = np.arange(outColor)
#Video stats
xdim, ydim = 1280, 720
fps	= 25
nFrame	= 6642	#number of frames in this video, found by FFprobe
num_pix	= xdim*ydim 	#=number of pixels in one frame
run_time= nFrame/fps	#=265.68 seconds
yoffset	= -0.25 + ydim/2	
vid	= "Arctic Monkeys - Do I Wanna Know- (Official Video).mp4"
#Used in this particular program:
nCo	= 60	#number of coefficient in fourier analysis
threshold=0.1 #if more than this fraction of c-colored line is missing, then it is considered invalid as a line.
DPI	= 80



'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''
minute = str( input( "minute?" ) ).zfill(2)
second = str( input( "second?" ) ).zfill(2)
duration=float(input("duration?"))

#Declare names (fig, ax) for the plotting methods.
fig = plt.figure(frameon=False)
fig.set_size_inches( int(xdim/DPI), int(ydim/DPI) )

ax = plt.Axes(fig, [0., 0., 1., 1.] )	#for lineIn_FTGraphOut: nCo/2 is the upper bound instead.
#Equiv of typing fig.set_tight_layout(True)
fig.add_axes(ax)
'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''



'''#declare classes██████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
def mono_framexyIn_analogueOut(mono_framexy):
	return mono_framexy>>7
#This program is so short I could've merged it into the function; but for clarity I'll keep it.

class FRAME:
	def __init__(self, frame_cxy): #frame_yx [color][y][x].		#Schematic diagram:
		self.red   = mono_framexyIn_analogueOut( frame_cxy[R] )	#intermediate colors
		self.green = mono_framexyIn_analogueOut( frame_cxy[G] )	#intermediate colors
		self.blue  = mono_framexyIn_analogueOut( frame_cxy[B] )	#intermediate colors
		self.yellow= self.green  * self.red			#intermediate colors
		self.white = self.yellow * self.blue			#white	oooooo
		self.blue  = self.blue   - self.white			#blue	----oo
		self.green = self.green  - self.yellow			#green	--oo--
		self.red   = self.red    - self.yellow			#red	oo----
		self.yellow= self.yellow - self.white			#yellow	oooo--
			#type(bool).color[x][y]



'''#Declare subprograms for extraction___██████████████████████████████████████████████████████████████████████████████████████████'''
def get_frames(m1, s1, d):	#input time, get one second worth of frames
	FFMPEG_BIN = "ffmpeg"
	#1. convert time
	if int(s1)==0:
		s1 = '59'
		m1 = str(int(m1)-1)
	else: s1 = str( (int(s1)-1) ).zfill(2)
	no_frame = int(d*fps)
	d = str(d)

	#2. open the video as a subprocess
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

	return snippet #[no. of frames][y(up-down)][x(left-right)][color]



'''#Declare Subprograms for frame manipulation███___████████████████████████████████████████████████████████████████████████████████'''
#for frame in Frames:
def multicolor_frameIn_multicolorLineOut(frame_yxc, xdim = xdim):
	#inheriting the parent's properties :)
	frame = FRAME( frame_yxc.T )
	multiLine = [[],]*outColor
	
	for C in range (outColor):
		monoframe = getattr( frame,cList[C] )	#monoframe[x][y]
		if np.sum( monoframe )==0:
			#A.case of having such colour at all:
			multiLine[C] = []
		else:
			for xcoord in range (xdim):
				multiLine[C].append( meanInd(monoframe[xcoord], targetWord='dum', safeWord = 'fail') )
			multiLine[C]= interpolate(multiLine[C], targetWord='dum', safeWord='fail', xdim=xdim)

			#print(cList[C],"is nonzero at", np.nonzero(monoframe))
			#print(cList[C],"frame is equal to", monoframe)

	return multiLine #[outColor][x]

def xynonzero(array):
	return np.array(np.nonzero(array)).T

def meanInd(vertical_column, targetWord = 'dum', safeWord='fail'):
	indices = np.nonzero(vertical_column)

	#catch the case were more than acceptable no. of lines are found.
	if np.std( vertical_column )>( threshold*len(vertical_column) ): return safeWord
	if len(indices)==0: return targetWord	#catch the case where no line is found.
	return np.mean(indices)

def interpolate( y, targetWord='dum', safeWord='fail', xdim = xdim ):
	fp= np.array(y)
	xp= np.arange(xdim)
	x = np.arange(xdim)

	mask = np.zeros(xdim, dtype = bool)
	for n in range (xdim):
		if y[n]!=targetWord:
			mask[n] = True	#Kill all elements except those containing actual values instead of the dummy target word.
		if y[n]==safeWord:
			return []	#stop the loop and return null if a safeWord is found.

	fp = fp[mask]
	xp = xp[mask]
	y = np.interp(x, xp, np.array(fp, dtype=float))
	return np.array(y, dtype=int)
#*Will have to find out how to stop showing these VisibleDeprecationWarning; I know why they exist(because I'm interpolating beyond the axis) but they are annoying.

def scaleShiftLine(line, yoffset=yoffset):
	return yoffset-np.array(line)



'''#Subprogram for Fourier transform██████___███████████████████████████████████████████████████████████████████████████████████████'''
#*Perhaps this needs more tweaking to ensure that both FFT and SlowFT give the same result, w/o the need to modify upperbounds.
def lineIn_FTGraphOut(y, xdim = xdim):
	if len(y)==0: return []

	func = [0] * nCo	#the product function to be integrated in the n-th harmonic.
	Coef = [0] * nCo	#note that the 0-th coefficient is used for cos instead of sine.
	for n in range (0, 1 ) :
		func[n] = lambda x : ((y[int(ceil(x))])*(x-floor(x))+y[int(floor(x))]*(ceil(x)-x))
		Coef[n] += (2/xdim)*inte(func[n], 0, xdim-1)[0]
	for n in range (1, nCo):
		func[n] = lambda x : np.sin(n*np.pi*x/xdim)*((y[int(ceil(x))])*(x-floor(x))+y[int(floor(x))]*(ceil(x)-x))
		Coef[n] += (2/xdim)*inte(func[n], 0, xdim-1)[0]
	return Coef

def lineIn_FastFTGraphOut(y):
	if len(y)==0: return []

	Coef = np.real(np.fft.rfft(y))/1000
	Coef = np.split(Coef, [nCo/2, len(Coef)])[0]
	#k = np.arange(nCo/2)
	return Coef

def smoothen(y_rough):
	a = len(y_rough)
	if a<2: return [[],[]]
	x_old = np.linspace(0, a, a) #assuming the y values are taken at constant intervals
	x_new = np.linspace(0, a, a*10)
	y_smooth = spline (x_old, y_rough, x_new)
	return (x_new, y_smooth)



'''#Subprogram for plotting█████████___████████████████████████████████████████████████████████████████████████████████████████████'''
def manualInitialize():
	(red, ) = ax.plot([], [], lw=3, color = 'r')
	(green,)= ax.plot([], [], lw=3, color = 'g')
	(blue,) = ax.plot([], [], lw=3, color = 'b')
	(yellow,)=ax.plot([], [], lw=3, color = 'y')
	(white,)= ax.plot([], [], lw=3, color = 'w')#Type of these lines are called "<class 'matplotlib.lines.Line2D'>"
	return (red, green, blue, yellow, white)



'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''
#Obtain raw data
Frames = get_frames(minute, second, duration) #global Frames
#outputs boolean array with max index [numFrame][ydim][xdim][color]

#Declaring line names and the collective name for all lines to be used below:
(red, green, blue, yellow, white) = manualInitialize()
lineCollection = (red, green, blue, yellow, white)
'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''



def init(): #Style setting
	#*not sure if I have to clear frame before starting or not.
	ax.set_axis_bgcolor((0, 0, 0))
	ax.set_xlim(0,nCo)	#equivalent to
	ax.set_ylim(-100,100)	#ax = plt.axes(xlim=(0, nCo), ylim=(-100,100))
	return lineCollection #Give back the same (global) varible that contains the list of lines.

'''#Main Controller program████████████___██████████████████████████████████████████████████████████████████████████████████████████'''
def frameIn_smoothLine(i):
	print("parsing frame", i+1)
	multiLine = multicolor_frameIn_multicolorLineOut(Frames[i])
	for n in range(outColor):
		FTgraph = lineIn_FastFTGraphOut(multiLine[n])	#*Delete the Frames[i] from memory somewhere?
		(k, smoothLines) = smoothen(FTgraph)
		lineCollection[n].set_data(k, smoothLines)
		#print(cList[n],r'\t',"line before transform has shape", np.shape(multiLine[n]))
	return lineCollection



'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''
anim = animation.FuncAnimation(fig, frameIn_smoothLine, init_func = init, frames = int(fps*duration), interval = 40, blit=True)
anim.save( minute+'_'+second+'_dur='+str(duration)+'.mp4', fps = 25, extra_args=['-vcodec', 'libx264'], dpi=DPI)
'''█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_█_'''
