from odbAccess import *

def function():
	'''
	trying 2 approaches here, first by calculating nodes assosciated with elements and getting the position from nodes and dislocation density from elements
	Orrrr just get dislocation density directly from getSubset(position Centroid)
	'''
	# step 1 determine positions of elements in grain 2. 
	print 'gets here 1'
	resultStringList = []
	
	#frameNo
	frameNo = 50
	
	odb = openOdb(path = 'cube_slow1000d_lime4hold.odb')
	grains = odb.rootAssembly.instances['PART-1-1'].elementSets
	mypathforoutput = 'U:/Group Studies/Research/'
	outputField = odb.steps['Step-1'].frames[frameNo].fieldOutputs
	'''
	#lets create a node set for every element in the model
	
	for grainNo in range(len(grains)):
	
		grain = grains['GRAIN_' + str(grainNo +1)]
		
		count = 0
		
		for elements in grain.elements:
			
			count = count + 1
			
			print elements.connectivity
			
			nodeSet = odb.rootAssembly.instances['PART-1-1'].NodeSetFromNodeLabels('GRAIN_'+str(grainNo+1) +'_nodesInElement_'+str(count),elements.connectivity)
			
		
	#notes on CoM, for a simplex is the average position of the vertexes. Nice and easy.
	'''
	coordOutputField = outputField['COORD']
	evolOutputField = outputField['EVOL']
	
	CentreOfVoid = []
	
	for grainNo in range(len(grains)):
	
		grain = grains['GRAIN_' + str(grainNo +1)]
		
		elementVolumes = evolOutputField.getSubset(region = grain).values
		grainVolume = 0
		
		averageGrainPosition = [0]*3
		#how do i know that the elementNo for element volumes and element nodes are the same? I believe its because im constructing them in exactly the same way... 
		for elementNo in range(len(grain.elements)):
			
			nodeSet = odb.rootAssembly.instances['PART-1-1'].nodeSets['GRAIN_'+str(grainNo+1)+'_nodesInElement_'+str(elementNo+1)]
			#
			elementNodes = coordOutputField.getSubset(region = nodeSet).values
				
			elementCentreOfMass = [0]*3
			#element center of mass is nice and easy to find for tetragons... important...
			for node in elementNodes:
				
				a = [0]*3
				
				a[0] = node.data[0]
				a[1] = node.data[1]
				a[2] = node.data[2]
				
				elementCentreOfMass[0] = elementCentreOfMass[0] + a [0] / len(elementNodes)
				elementCentreOfMass[1] = elementCentreOfMass[1] + a [1] / len(elementNodes)
				elementCentreOfMass[2] = elementCentreOfMass[2] + a [2] / len(elementNodes)
			
			#might be worth weighting by element volume sure why not..
			
			elementVol = elementVolumes[elementNo].data
			grainVolume = grainVolume + elementVol
			
			averageGrainPosition[0] = averageGrainPosition[0] + elementCentreOfMass[0] * elementVol
			averageGrainPosition[1] = averageGrainPosition[1] + elementCentreOfMass[1] * elementVol
			averageGrainPosition[2] = averageGrainPosition[2] + elementCentreOfMass[2] * elementVol
		
		averageGrainPosition[0] = averageGrainPosition[0] / grainVolume
		averageGrainPosition[1] = averageGrainPosition[1] / grainVolume
		averageGrainPosition[2] = averageGrainPosition[2] / grainVolume
		
		if (grainNo == 0):
		
			CentreOfVoid = averageGrainPosition
		
		result = (CentreOfVoid[0] - averageGrainPosition[0])*(CentreOfVoid[0] - averageGrainPosition[0]) + (CentreOfVoid[1] - averageGrainPosition[1])*(CentreOfVoid[1] - averageGrainPosition[1]) + (CentreOfVoid[2] - averageGrainPosition[2])*(CentreOfVoid[2] - averageGrainPosition[2]) 
		
		resultStringList.append('GRAIN_'+str(grainNo+1)+'   '+str(result) + '\n')		
		
		#print ( 'Distance from Centre of Void Grain_' + str(grainNo) + '   ' + str(averageGrainPosition))
		
		print ( 'Distance from Centre of Void Grain_' + str(grainNo) + '   ' + str(result))
		
	outFile_ev=open(mypathforoutput + "GrainDistanceFromCentreOfVoidFrame" + str(frameNo) + ".txt",'w')
	
	for n in range(len(resultStringList)):
			
		outFile_ev.write(resultStringList[n])			
		
	outFile_ev.close()
	
	
	
	odb.close

if __name__ == '__main__':
	
	function()	