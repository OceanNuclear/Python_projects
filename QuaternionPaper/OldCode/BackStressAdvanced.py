
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
	#thisjob = 'cube125_1000C_SLOW_4_UVARMb/cube125_1000C_SLOW_4_UVARMb.odb'
	
	#useful definitions and important initialisations
	
	
	
	spaces = '   '
	#odb = openOdb(path = thisjob)
	
	for n in range(8):
		outputText = []
		
		odb = openOdb(path = 'grain_step1_g' + str(n+1) + '.odb')
		
		my_csys = odb.rootAssembly.DatumCsysByThreePoints(name='my_csys', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0), point1=(1, 0, 0), point2=(0, 1, 0))
		elemsets = odb.rootAssembly.instances['PART-1-1'].elementSets
	
		
		elemSet = elemsets['GRAIN_1']
		
		i = -1
		
		for frame in odb.steps['Step-1'].frames:
			
			
			i = i +1
			
			stressField = frame.fieldOutputs['S'].getTransformedField(datumCsys=my_csys).getSubset(region = elemSet)
			
			stressList = [0]*6
			
			for ipStressTensor in stressField.values:
					
				for elementIndex in range(6):
					
					stressList[elementIndex] += ipStressTensor.data[elementIndex]
					
			stressList = [x / len(stressField.values) for x in stressList]
			
			outputText.append(str(stressList[0]) +'   ' + str(stressList[1])+'   ' +str(stressList[2])+'   ' +str(stressList[3])+'   ' +str(stressList[4])+'   ' +str(stressList[5]) + '\n')
			
			print outputText[i]
	
		outFile_ev = open(mypathforoutput + 'MONO_'+ str(n+1) + "_GRAIN_StressTensorsStep1.txt",'w')
		
		for n in range(len(outputText)):
			
			outFile_ev.write(outputText[n])			
		
		outFile_ev.close()
	

		
	print 'reaches past outputting code' 
		
	'''
	'''
	odb.close()
	
if __name__ == '__main__':
	
	function()	