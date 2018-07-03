#For this code i need to extract the stress tensor for the whole RVE
#Calculate Difference between this tensor and the stress Tensors of Individual Grains
#Then either calculate some total scalar measure of back stress by summing von mises stresses of grains ORRRR
#Just Extract Grain Number and backstress assosciated ~ do this first

from odbAccess import *
import numpy as np
from sys import argv,exit
'''Usage: abq6131 python grainDislocationDensity.py'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def function():

	#specifying paths and jobs
	mypath = 'C:/SIMULIA/Abaqus/Commands/'
	mypathforoutput = 'F:/Group Studies/Work Package 4/RawData/'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb/cube125_1000C_SLOW_4_UVARMb.odb'
	
	#useful definitions and important initialisations
	
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')

	elemsets = odb.rootAssembly.instances['PART-1-1'].elementSets
	my_csys = odb.rootAssembly.DatumCsysByThreePoints(name='my_csys', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0), point1=(1, 0, 0), point2=(0, 1, 0))
	
	outputText = []
	
	for step in odb.steps.values():
	
		for frame in step.frames:
			
			#frame = odb.steps.values()[0].frames[frameNo]
			StressField = frame.fieldOutputs['S'].getTransformedField(datumCsys=my_csys)
			
			#calculate total homo stress
			
			MacroStress = [0]*6
			
			print 'calculating MacroStress at frame time' +str(frame.frameValue)
			
			for StressTensor in StressField.values:
				
				for elementIndex in range(len(MacroStress)):
					
					MacroStress[elementIndex] += StressTensor.data[elementIndex]
			
			MacroStress = [x / len(StressField.values) for x in MacroStress]
			
			BackStressList = []
			
			for i in range(len(elemsets)):
				
				elemset = elemsets['GRAIN_'+ str(i+1)]
				
				grainStressField = StressField.getSubset(region = elemset)
				
				microStress = [0]*6
				for ipStressTensor in grainStressField.values:
					
					for elementIndex in range(len(microStress)):
					
						microStress[elementIndex] += ipStressTensor.data[elementIndex]
						
				microStress = [x / len(grainStressField.values) for x in microStress]
				
				BackStress = []
				
				for Index in range(len(MacroStress)):
				
					BackStress.append(microStress[Index] - MacroStress[Index])
				
				VonMisesBackStress = (0.5*((BackStress[0]-BackStress[1])**2 + (BackStress[1]- BackStress[2])**2 + 6*(BackStress[3]**2 + BackStress[4]**2 + BackStress[5]**2)))**0.5
				print VonMisesBackStress
				BackStressList.append(VonMisesBackStress)
				
			TotalBackStressInList = np.sum(BackStressList)
			
			print ('time: ' + str(frame.frameValue) + '   ' + str(TotalBackStressInList))
			
			outputText.append(str(TotalBackStressInList) + '\n')
		
	outFile_ev = open(mypathforoutput + "BackStressesOverTime_Unaxial.txt",'w')
		
	print 'reaches past outputting code' 
		
	for n in range(len(outputText)):
		
		outFile_ev.write(outputText[n])			
	
	outFile_ev.close()
		
	odb.close()
	
if __name__ == '__main__':
	
	function()	