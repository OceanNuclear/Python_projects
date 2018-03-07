def plotGeodesic(theta1, phi1, theta2, phi2):
	#Cross product the two points, duh.
	#That'll give ctheta and cphi.
	Theta, Phi = [],[]
	R, Angle = PointPlotter(Theta, Phi)
	return 

def Fitter():
	scipy.curve_fit(InverseFinder, R, Angle, )
	print(y[0],y[1])
	return

def getInput():
	ConversionFactor=pi/180

	Theta=float(input("Theta in degrees (0<=Theta<=90)="))
	if math.ceil(Theta/90)==1 or math.floor(Theta/90)==0:	Theta = Theta *ConversionFactor
	else:	raise ValueError

	Phi = float( input("no. of degrees=") )
	Phi = Phi*ConversionFactor

	return Theta , Phi

