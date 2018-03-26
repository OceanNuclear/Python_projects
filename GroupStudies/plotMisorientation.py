#!/home/oceanw/anaconda3/bin/python3
#Simple plotter to plot the misorientaiton.
import numpy as np
import matplotlib.pyplot as plt



def plot(inFile,average='min',color='blue'):
	numLines = sum(1 for line in open(inFile))

	x = np.zeros(numLines)
	y = np.zeros(numLines)

	f = open(inFile, "r")
	f.seek(0)
	Data = f.readlines()
	f.close()

	for line in range (numLines):
		x[line] = Data[line].split()[0]
		y[line] = Data[line].split()[1]

	#plot You can format it as #'{:0=3.0f}'.format( spectrum*10 )
	t = str(inFile[-7:-4]+average)
	#plt.plot(x,y,label=t, color=color, alpha = 0.8)
	plt.plot(x,y, alpha = 0.8)
	return

def plotIndividual(inFile, outFile):
	numLines = sum(1 for line in open(inFile))

	x = np.zeros(numLines)
	y = np.zeros(numLines)

	f = open(inFile, "r")
	f.seek(0)
	Data = f.readlines()
	f.close()

	for line in range (numLines):
		x[line] = Data[line].split()[0]
		y[line] = Data[line].split()[1]

	#plot You can format it as #'{:0=3.0f}'.format( spectrum*10 )
	t = str("scatter in grain"+inFile[-7:-4])
	graph.set_data( x, y)
	plt.savefig(outFile)
	return



numGrain = 124
cList = ('r','darkgreen','b','darkslategrey','black','purple','darkred')
n = 0
'''
plt.suptitle("Misorientation from renormalized average for every grain")
plt.title("\n On average, number of radians required to rotate \n from Gauss point to the average orientation in grain")
plt.ylabel("misorientation (radian)")
plt.xlabel("time (s)")
ax = plt.subplot(111)
ax.set_xlim([0,5469])
ax.set_ylim([0,0.1])
[graph,] = ax.plot([],[])

for grain in range (numGrain):
	grain = str('{:0=3d}'.format(grain+1))
	plotIndividual("Scatter/min/ScatterInGrain"+grain+".txt","Scatter/min/ScatterInGrain"+grain+".png")
	#I'll admit that I don't know why it comes up with an error message?
	print("grain",grain,"is being plotted.")
'''

if __name__=="__main__":
	fig = plt.figure()
	
	for grain in range (numGrain):
		grain = str('{:0=3d}'.format(grain+1))
		#if (grain!='052')and(grain!='114')and(grain!='073'):
			#shows up as discontinuities+jagged in the renormalized method
			#and jagged in the minimization method
		#Apart from these, for both types of average, 035 and 104 are also doing the wibbly wobbly (jagged) stuff!
		#Moreorver, jagged-ness showed up in 062, 088, but only for minimization method.
		if True:
		#if np.sum([grain==x for x in ['052','073','114','035','104','062','088']]):
			print("plotting grain", grain)
			#plot("Scatter/renormalized/ScatterInGrain"+grain+".txt", average='renormalized',color=cList[n])
			#plot("Scatter/min/ScatterInGrain"+grain+".txt",color=cList[n])
			plot("Scatter/min/ScatterInGrain"+grain+".txt")
			n+=1
	
	#plot("Scatter/min/TotalNormalizedScatter.txt")	#
	plt.suptitle("Misorientation from minimized average for every grain")
	plt.title("\n On average, number of radians required to rotate \n from Gauss point to the average orientation in grain")
	plt.ylabel("misorientation (radian)")
	plt.xlabel("time (s)")
	plt.legend(loc=6)
	#fig.set_size_inches([11.2,8.4])
	#fig.set_size_inches([16.8,12.6])
	ax = plt.subplot(111)
	ax.set_ylim([0,0.1])
	ax.set_xlim([-5,5469.0])
	plt.savefig("Scatter/min/DeviationFromMinAvgSelectedsmall.png")	#
	#plt.show()
