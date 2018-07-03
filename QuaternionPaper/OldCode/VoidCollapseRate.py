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
	mypathforoutput = 'U:/Group Studies/Research/'
	thisjob = 'n25hip_1_slow1000_hold_lim55b2.odb'
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
	
	stepTempTime = 0
	
	for stepNo in range(len(steps)):
	
		frames = steps['Step-'+str(stepNo + 1)].frames
		
		for frame in frames:
			
			time = stepTempTime + frame.frameValue
			
			fieldOUTPUTS = frame.fieldOutputs
			
			volumeValues = fieldOUTPUTS['EVOL'].getSubset(region = voidgrain).values
			
			volume = 0
			
			for j in range(len(volumeValues)):
				 
				volume = volume + volumeValues[j].data
			
			if (i == 0 ) or (i == 68): 
			
				dvBydt = 0
			
			else:
				dvBydt = (previousVolume - volume)/ (time - previousTime)
			
			DataList.append(dvBydt)
			
			datapoint = str(DataList[i])
			
			outputText.append(str(time) + '   ' + str(DataList[i]) + '\n')
			
			print('Frame ' + str(i+1) + ':\n'+ 'Time= ' + str(time) + '\n' + 'dvBydt= ' + datapoint + '\n')
			
			i = i + 1
			
			previousTime = time 
			
			previousVolume = volume
			
		stepTempTime = time
		
	outFile_ev=open(mypathforoutput + "VoidCollapseRateOverTime2.txt",'w')
	
	for n in range(len(outputText)):
			
		outFile_ev.write(outputText[n])			
		
	outFile_ev.close()
	
	odb.close()
	
if __name__ == '__main__':
	
	function()	
