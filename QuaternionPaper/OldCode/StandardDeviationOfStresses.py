from odbAccess import *
import numpy as np
from sys import argv,exit

'''Usage: abq6131 python extractRotations.py'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def function():
	
	#specifying paths and jobs
	mypath = 'C:/SIMULIA/Abaqus/Commands/'
	mypathforoutput = 'F:\Group Studies\Work Package 3\RawData'
	#thisjob = 'different_orientations/n25hip_2_slow1000_hold_lim55b2.odb'
	#thisjob = 'different_orientations/n25hip_3_slow1000_hold_lim55b2.odb'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb\cube125_1000C_SLOW_4_UVARMb.odb'

	#useful definitions and important initialisations
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')
	#defining the model sets
	elementSets = odb.rootAssembly.instances['PART-1-1'].elementSets
	
	outputText = []
	
	DataList = []
	
	#print len(voidgrain_)
	
	steps = odb.steps
	
	i = 0
	
	temptime = 0
	
	for step in steps.values():
	
		frames = step.frames
		
		for frame in frames:
			
			time = temptime + frame.frameValue
			
			fieldOUTPUTS = frame.fieldOutputs
			
			CalcList = []
			
			for grainNo in range(len(elementSets)):
			
				thisGrain = odb.rootAssembly.instances['PART-1-1'].elementSets['GRAIN_' + str(grainNo + 1)]
			
				SValues = fieldOUTPUTS['S'].getSubset(region = thisGrain).values
				
				for j in range(len(SValues)):
					 
					 CalcList.append(SValues[j].mises)
				
			DataList.append(np.std(CalcList))
			
			datapoint = str(DataList[i])
			
			outputText.append(str(time) + '   ' + str(DataList[i]) + '\n')
			
			print('Frame ' + str(i+1) + ':\n'+ 'Time= ' + str(time) + '\n' + 'StdOfStress= ' + datapoint + '\n')
			
			i = i + 1
		
		temptime = time
		
	outFile_ev=open(mypathforoutput + "\stdStressesUnaxial",'w')
	
	print 'successfully opened file'
	
	for n in range(len(outputText)):
			
		outFile_ev.write(outputText[n])			
		
	outFile_ev.close()
	
	odb.close()
	
if __name__ == '__main__':
	
	function()	
