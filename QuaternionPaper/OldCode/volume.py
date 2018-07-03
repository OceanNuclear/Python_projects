from odbAccess import *
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
	thisjob = 'n25hip_321_slow1000_hold_lim55b2.odb'

	#useful definitions and important initialisations
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')
	#defining the model sets
	elemSets = odb.rootAssembly.instances['PART-1-1'].elementSets
	
	outputText = []
	
	DataList = []
	
	voidgrain = elemSets['GRAIN_1']
	#print len(voidgrain_)
	
	steps = odb.steps
	
	i = 0
	
	temptime = 0
	
	for stepNo in range(len(steps)):
	
		frames = steps['Step-'+str(stepNo + 1)].frames
		
		for frame in frames:
			
			time = temptime + frame.frameValue
			
			fieldOUTPUTS = frame.fieldOutputs
			
			volumeValues = fieldOUTPUTS['EVOL'].getSubset(region = voidgrain).values
			
			volume = 0
			
			for j in range(len(volumeValues)):
				 
				volume = volume + volumeValues[j].data
			
			DataList.append(volume)
			
			datapoint = str(DataList[i])
			
			outputText.append(str(time) + '   ' + str(DataList[i]) + '\n')
			
			print('Frame ' + str(i+1) + ':\n'+ 'Time= ' + str(time) + '\n' + 'Volume= ' + datapoint + '\n')
			
			i = i + 1
		
		temptime = time
		
	outFile_ev=open(mypathforoutput + "\VoidVolumeOverTime_321",'w')
	
	print 'successfully opened file'
	
	for n in range(len(outputText)):
			
		outFile_ev.write(outputText[n])			
		
	outFile_ev.close()
	
	odb.close()
	
if __name__ == '__main__':
	
	function()	
