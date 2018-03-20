#!/home/oceanw/anaconda3/bin/python
'''THIS IS A VERY COMPUTATIONALLY INTENSIVE SCRIPT! You have been warned.'''
#Takes up to 1 minute per 3 frames when ran for the first time.
from numpy import sin, cos, tan, arccos, arctan, sqrt, pi
import numpy as np
import matplotlib.pyplot as plt
from quat import *
tau = 2*pi
from generalLibrary import *
debug = False
normal= not debug
Taylor= False
graphicalAvg = False
everyPoint = False
WanderOutside=False
from scipy.optimize import minimize
import time, os



startTime = time.time()
def naturalNum(Index):
	if np.sign(Index)!=-1: return Index
	else: return 0
#Background plotting functions
def plotCircle(cTheta, cPhi):
	Theta, Phi = DrawCircle(cTheta , cPhi , a=pi/2) #Theta has to be restricted to less than pi/2
	R, Angle = stereographicProjector(Theta, Phi)

	X, Y = polar2D_xy(Angle, R)
	ax.plot(X,Y, color='black', linestyle=':')
	return [R,Angle]

def plotDiag(phi):
	X,Y = Diag_xy(phi, 0,1)
	ax.plot( X,Y , color='black', linestyle=':')
	return

def plotDiag2(phi):
	X,Y = Diag_xy(phi, pi/6,1)
	ax.plot( X,Y , color='g')

def BG(CompletePoleFig=False):
	InversePoleFig= not CompletePoleFig
	if CompletePoleFig:
		for n in range (8):
			ax.plot(Diag_xy(n*pi/8), color = black, linestyle = ':')
			if not (n&0x1): #for even cases, plot the circles.
				plotCircle(pi/4, n*tau/8)
			'''
			if(n&0x1): #for odd cases, plot diagonals and vertices.
				plotDiag2(n*tau/8)
				PointPlotter(0.96 , n*tau/8)
			'''

	if InversePoleFig: #Plot the boundary of Inverse pole figure
		X,Y = InversePoleFigureLine()
		ax.plot(X, Y, color='black')#, lw=0.8

		x_an, y_an = getIPtip()
		
		ax.annotate("[001]",	xy=[0,0], xycoords='data', ha='right',	color = 'black')
		ax.annotate("[101]",	xy=[tan(pi/8),0],xycoords='data',	color = 'black')
		ax.annotate("[111]",	xy=[x_an,y_an],	xycoords='data',	color = 'black')
		'''
		ax.annotate("and the four corners",	xy=[pi/4 -np.deg2rad(30), 0.44 ],color = 'r'	)
		ax.annotate("of the top half of the cube",xy=[pi/4 -np.deg2rad(40),0.43],color = 'black')
		'''
	return



#Controller bit
'''█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'''
if __name__=="__main__":
	global fig
	fig = plt.figure()
	fig.set_tight_layout(True)

	global ax
	ax = plt.subplot(111)
	#ax = plt.Axes(fig, [0., 0., 1., 1.] )
	ax.axis('off')
	counter = 0
	def incr():
		global counter
		counter+=1
		print("Iteration",counter)
		return

	xlimits = expandAxisLimit(0, tan(pi/8))
	ylimits = expandAxisLimit(0,0.366) #0.366 is calculated above in the wasted bit of script (currently line 93)
	ax.set_xlim(xlimits)
	ax.set_ylim(ylimits)

	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_aspect(0.366/tan(pi/8))

	BG()

	RotationMatrices = ReadR("LiterallyEveryPoint/1FrameRotationMatrices.txt")

	numGrains = len(RotationMatrices)
	numGauss = 8

	ID = np.ones(int(numGrains/numGauss), dtype=int)*48
	#The max has range=(0,47), so in theory when ID has been introduced none of them should remain as 48.

	preNumFrame=0
	numFrame = 397
	ax.set_title("Evolution of grains orientations up to frame"+str(numFrame)+"out of 397 frames with symmetry averaging")

	qOfPoints=np.zeros([numGrains,4])
	x_line = np.zeros([numGrains,numFrame])
	y_line = np.zeros([numGrains,numFrame])

	x_avg = np.zeros([int(numGrains/numGauss),numFrame])
	y_avg = np.zeros([int(numGrains/numGauss),numFrame])

	distance=np.zeros([numGrains,numFrame])
	thresholdDistance = 0.02

	for combinedGrain in range(int(numGrains/numGauss)):	#iterate over the first frame's grains
		RList = RotationMatrices[combinedGrain*numGauss:(combinedGrain+1)*numGauss]	#get the initial list in 
		qList = []
		for R in RList:
			qList.append(RotToQuat(R))
		guessQuat = uglyAverage(qList)
		ThreeVar0 = Q_ThreeVar(guessQuat)

		print("Finding the ID of grain", combinedGrain)

		def misorientationSum(ThreeVar): #Define program to find the degrees of misorientation for a given input
			totalMisor = 0
			avg_q = ThreeVar_Q(ThreeVar)	#ThreeVar==[theta,THETA,PHI]
			for gau in range (numGauss):	#add up the 8 points's minimum misorientation
				totalMisor += misorientationSymm(avg_q,qList[gau])[0]
				#totalMisor += misorientation2(avg_q,qList[gau])
			return totalMisor

		bnds = [0,pi],[0,pi],[0,tau]	#set boundary for 
		ThreeVar_avg = minimize(misorientationSum, x0=ThreeVar0, bounds=(bnds)).x
		#dummy input of x=0, to get y = 0

		avg_q = np.nan_to_num(ThreeVar_Q(ThreeVar_avg))		#Get it in quaternion form
		R = QuatToR(avg_q)					#turn it into R (matrix) form
		v48 = R_v(R)
		ID[combinedGrain] = getIPpointID(v48)

		r = v48[ID[combinedGrain]]
		[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])
		R, Angle = stereographicProjector(Theta,Phi)

		X, Y = polar2D_xy(Angle, R)

		ax.plot(X, Y , marker = 'o', markerfacecolor='none', markeredgecolor='black')
		'''
		ax.annotate("",xy=(X2, Y2), xycoords='data',
			xytext=( X, Y ), textcoords='data',
			arrowprops=dict(arrowstyle="-",connectionstyle="arc3")
			)
		'''

	for frame in range (preNumFrame,numFrame):	#Iterate over frame
		fileName = "LiterallyEveryPoint/"+str(frame+1)+"FrameRotationMatrices.txt"
		fileNameOut= "MinimizedMatricesSymm/"+str(frame+1)+"FrameRotationMatrices.txt"
		fileNameNext="MinimizedMatricesSymm/"+str(frame+2)+"FrameRotationMatrices.txt"

		UpdatedMatrices = ReadR(fileName)	#Read the list of matrices for that frame

		if (not os.path.exists(fileNameNext) ) or (not os.path.exists(fileNameOut)):	#If either does not exist.
			for grain in range(numGrains):
				qOfPoints[grain] = RotToQuat(UpdatedMatrices[grain])	#Find the pose in terms of quaternion.

			toFile = ""
			for combinedGrain in range(int(numGrains/numGauss)):	#loop 8 gauss points at a time.
				print("Processing grainIndex=",'{:0=3d}'.format(combinedGrain),"/",int(numGrains/numGauss)-1,
					"; frame",'{:0=3d}'.format(frame+1),"/", numFrame)
				qList = qOfPoints[combinedGrain*numGauss:combinedGrain*numGauss+numGauss]
				guessQuat = uglyAverage(qList)
				ThreeVar0 = Q_ThreeVar(guessQuat)

				def misorientationSum(ThreeVar): #Define program to find the degrees of misorientation for a given input
					totalMisor = 0
					avg_q = ThreeVar_Q(ThreeVar)	#ThreeVar==[theta,THETA,PHI]
					for gau in range (numGauss):	#add up the 8 points's minimum misorientation
						#totalMisor += misorientation2(avg_q,qList[gau])
						totalMisor += misorientationSymm(avg_q,qList[gau])[0]
					return totalMisor

				bnds = [0,pi],[0,pi],[0,tau]
				ThreeVar_avg = minimize(misorientationSum, x0=ThreeVar0, bounds=(bnds)).x
				#dummy input of x=0; aim to get y = 0

				avg_q = np.nan_to_num(ThreeVar_Q(ThreeVar_avg))		#Get it in quaternion form

				theta_avg,THETA_avg,PHI_avg = ThreeVar_avg
				toFile += writeR(theta_avg,THETA_avg,PHI_avg)	#Write down the matrix

				R = QuatToR(avg_q)					#turn it into R (matrix) form
				r = R_v(R)[ID[combinedGrain]]				#Choose the appropriate grain

				if not WanderOutside:
					rList = R_v(R)				
					r = chooseIPpoint(rList)		#Choose point that falls on IP from the list

				[Theta, Phi] = cartesian_spherical( r[0], r[1], r[2])	#Convert from v to 3D(polar)
				R, Angle = stereographicProjector(Theta,Phi)		#Convert from 3D(polar) to 2D(polar)
				X, Y = polar2D_xy(Angle, R)				#Convert from 2D(polar) to 2D(cartesian)
				x_avg[combinedGrain][frame] = X	#add to list
				y_avg[combinedGrain][frame] = Y

				if debug:
					dx = X - x_avg[combinedGrain][naturalNum(frame-1)]
					dy = Y - y_avg[combinedGrain][naturalNum(frame-1)]
					distance[grain][frame] = RootSumSq([ dx , dy ])
					if distance[combinedGrain][frame]>thresholdDistance:
						print("Anomaly detected at grain with index",grain,"at frame",frame+1,
						"! This is because a distance of",'{:0=3.3f}'.format(distance[grain][frame]),
						"is measured between frames.")
						print("Previous frame is plotted at x=",x_line[combinedGrain][frame-1],
						", y=",y_line[combinedGrain][frame-1],
						"on the polar coordinate system, transformed to xy coordinates.")
						print(" Current frame is plotted at x=", x_line[combinedGrain][frame],
						", y=",y_line[combinedGrain][frame],
						"on the polar coordinate system, transformed to xy coordinates.")
			f=open(fileNameOut,"w")
			f.write(toFile)
			f.close()
			
		else:
			MinimizedMatrix=ReadR(fileNameOut)	#Read the existing rotation matrices and move on.
			print("Reading from frame",frame+1)
			for combinedGrain in range (len(MinimizedMatrix)):
				r =R_v( MinimizedMatrix[combinedGrain] )[ID[combinedGrain]]
				[Theta, Phi] = cartesian_spherical(r[0],r[1],r[2])
				R, Angle = stereographicProjector(Theta,Phi)
				X,Y = polar2D_xy(Angle,R)
				x_avg[combinedGrain][frame]=X
				y_avg[combinedGrain][frame]=Y

	#Now plot the lines, grain by grain.
	for combinedGrain in range(int(numGrains/numGauss)):
		ax.plot(x_avg[combinedGrain][preNumFrame:], y_avg[combinedGrain][preNumFrame:], color = 'black', lw = 0.7)

	print("Time taken = ",time.time()-startTime)

	if Taylor:
		linex, liney = [""]*5, [""]*5
		linex[0], liney[0] = getTaylorCurveDiv()[:,:]
		linex[1], liney[1] = getTaylorCurve2()[:,:]
		for n in range (3):
			linex[2+n], liney[2+n] = getTaylorCurve3()[:,n,:]
		for n in range (5):
			ax.plot(linex[n][:-1], liney[n][:-1], 'r', alpha = 0.5)
			ax.annotate("",xy=[linex[n][-2],liney[n][-2]], xytext =[linex[n][-1],liney[n][-1]], arrowprops=dict(color = 'r', arrowstyle= '<-'), alpha = 0.5)
		ax.set_title("Evolution of grains orientations up to frame"+str(numFrame)+"out of 397 frames \n compared with Taylor Model prediction (in red)")
		ax.set_aspect(0.366/tan(pi/8))
		#plt.show()
		fig.set_size_inches([11.2,8.4])
		plt.savefig("Graphs/OrientationEvolutionPlot/MinimizeAngle/GrainOrientationEvolution_ToFrame"+str(numFrame)+"misorientationMinimizationAverageWithTaylorModel.png")
	else: 	
		#plt.show()
		fig.set_size_inches([25.6,19.2])
		#fig.set_size_inches([11.2,8.4])
		if not WanderOutside:	plt.savefig("Graphs/OrientationEvolutionPlot/MinimizeAngle/GrainOrientationEvolution_ToFrame"+str(numFrame)+"misorientationMinimizationAverageWithSymmetry(Restricted).png")
		else:	plt.savefig("Graphs/OrientationEvolutionPlot/MinimizeAngle/GrainOrientationEvolution_ToFrame"+str(numFrame)+"misorientationMinimizationAverageWithSymmetry.png")
