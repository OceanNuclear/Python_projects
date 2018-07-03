from odbAccess import *
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
	mypathforoutput = 'F:/Group Studies/Work Package 5/RawData/'
	thisjob = 'cube125_1000C_SLOW_4_UVARMb\cube125_1000C_SLOW_4_UVARMb.odb'
	
	#useful definitions and important initialisations
	
	spaces = '   '
	odb = openOdb(path = thisjob)
	
	print('functioning')

	elemsets = odb.rootAssembly.instances['PART-1-1'].elementSets

	
	
	frameNoList = [15,30,45,60]
	
	for frameNo in frameNoList:
		
		print frameNo
		
		outputText = []
		
		for i in range(len(elemsets)):
			
			elemset = elemsets['GRAIN_'+ str(i+1)]
			#silly for loop but cba to unindent
			
			for a in range (0,1):
				step = odb.steps.values()[0]
				#print 'Processing Step:',step.name
				
				frames = step.frames
				
				frame = frames[frameNo]
				
				#print ('hasnt failed yet')
				
				#define dislocation field for each of the 12 slip systems... I could have made this a list for easier iteration in the future...
				
				SDVFieldList = []
				
				for fieldNo in range(12): 
				
					SDVFieldList.append(frame.fieldOutputs['SDV'+str(25+fieldNo)].getSubset(region = elemset))
				
				sum = 0
				
				for integrationPoints in range(len(SDVFieldList[0].values)):
					
					for SDVField in SDVFieldList:
					
						sum = sum + SDVField.values[integrationPoints].data
				
				sum = sum/(len(SDVFieldList[0].values))
				
				print ('dislocations in grain ' + str(i+1) + ' = ' + str(sum) + '\n' )
				#outputText.append('GRAIN_' + str(i+1) +spaces+str(sum)+'\n')
				outputText.append(str(sum)+'\n')
				
		
		outFile_ev = open(mypathforoutput + "DislocationGenerationFrame" + str(frameNo+60) + "UnaxialNew.txt",'w')
		
		print 'reaches past outputting code' 
		
		for n in range(len(outputText)):
		
			outFile_ev.write(outputText[n])			
			
		outFile_ev.close()
	
	odb.close()
	
if __name__ == '__main__':
	
	function()	