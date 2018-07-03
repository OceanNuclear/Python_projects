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
	
	#specifying job
	thisjob = 'n25hip_1_slow1000_hold_lim55b2.odb'
	#useful definitions and important initialisations
	odb = openOdb(path = thisjob)
	elemSets = odb.rootAssembly.instances['PART-1-1'].elementSets
	print('functioning')
	#defining the model sets
	elemsets = odb.rootAssembly.instances['PART-1-1'].elementSets
	
	frameno1 = odb.steps['Step-1'].frames	#no of frames for each step
	frameno2 = odb.steps['Step-2'].frames	#
	

	file = open("data.txt","w")
	
	
	
	i = 0
	
	print ('Writing frame numbers')
	
	file.write('Frame:')
	
	for i in range(len(frameno1)):	
		file.write(' ' + str(i))
	
	i = 0
	file.write(' Step_2')
	
	for i in range(len(frameno2)):	
		j = i + len(frameno1)
		file.write(' ' + str(j))
	
	file.write('\n')
	
	print ('...done\n')
	
	print ('Writing times')
	
	file.write('Time:')
	
	i = 0
	
	for i in range(len(frameno1)):	
		frame = odb.steps['Step-1'].frames[i]
		time = frame.frameValue
		file.write(' ' + str(time))
	
	t = time
	
	i = 0
	
	file.write(' Step_2')
	
	for i in range(len(frameno2)):	
		frame = odb.steps['Step-2'].frames[i]
		time = frame.frameValue + t
		file.write(' ' + str(time))	
	
	
	file.write('\n')
	
	print ('...done\n')
	
	f = len(frameno1) + len(frameno2)
	
	RVE_stress = [0]*f																			#reset stress, strain, and volume variables over RVE	
	RVE_strain_plastic = [0]*f
	RVE_strain_elastic = [0]*f
	
	g = len(elemsets)
	
	#for j in range(len(elemsets)-1): 														#for hip model
	for j in range(len(elemsets)): 															#for uniaxial model

		#grain = 'GRAIN_' + str(j+2)														#for hip model
		grain = 'GRAIN_' + str(j+1)															#for uniaxial model
	
		print ('Writing data for ' + str(grain))
	
		this_grain = elemsets[grain]														#specify which grain to look at	
	
		file.write(str(grain) + ':')
		
		
	
		for i in range(len(frameno1)):

			frame = odb.steps['Step-1'].frames[i]				
			fieldOUTPUTS = frame.fieldOutputs
			stress_points = fieldOUTPUTS['S'].getSubset(region = this_grain).values 		#stress on integration points within set grain
			elastic_strain_points = fieldOUTPUTS['EE'].getSubset(region = this_grain).values	#strain on integration points within set grain
			plastic_strain_points = fieldOUTPUTS['PE'].getSubset(region = this_grain).values
			
			
			sum_strain_elastic = 0
			sum_strain_plastic = 0
			sum_stress = 0
			n = len(stress_points)
			k = 0
			
			for k in range(len(stress_points)):												#loop to sum variables
			
				volume_stress = ((stress_points[k].mises)/n)								#normalise stress
				volume_strain_elastic = (((elastic_strain_points[k].mises)/n))
				volume_strain_plastic = (((plastic_strain_points[k].mises)/n))
				sum_stress = sum_stress + volume_stress
				sum_strain_elastic = sum_strain_elastic + volume_strain_elastic
				sum_strain_plastic = sum_strain_plastic + volume_strain_plastic
			file.write(' ' + str(sum_stress))
			RVE_stress[i] = RVE_stress[i] + (sum_stress/g)
			RVE_strain_elastic[i] = RVE_strain_elastic[i] + (sum_strain_elastic/g)
			RVE_strain_plastic[i] = RVE_strain_plastic[i] + (sum_strain_plastic/g)
			
		i = 0
		file.write(' ')
		
		for i in range(len(frameno2)):

			z = i + len(frameno1)

			frame = odb.steps['Step-2'].frames[i]				
			fieldOUTPUTS = frame.fieldOutputs
			stress_points = fieldOUTPUTS['S'].getSubset(region = this_grain).values 		#stress on integration points within set grain
			elastic_strain_points = fieldOUTPUTS['EE'].getSubset(region = this_grain).values	#strain on integration points within set grain
			plastic_strain_points = fieldOUTPUTS['PE'].getSubset(region = this_grain).values
			
			
			sum_strain = 0
			sum_stress = 0
			n = len(stress_points)
			k = 0
			
			for k in range(len(stress_points)):												#loop to sum variables
			
				volume_stress = ((stress_points[k].mises)/n)								#normalise stress
				volume_strain_elastic = (((elastic_strain_points[k].mises)/n))
				volume_strain_plastic = (((plastic_strain_points[k].mises)/n))
				sum_stress = sum_stress + volume_stress
				sum_strain_elastic = sum_strain_elastic + volume_strain_elastic
				sum_strain_plastic = sum_strain_plastic + volume_strain_plastic
			file.write(' ' + str(sum_stress))
			RVE_stress[z] = RVE_stress[z] + (sum_stress/g)
			RVE_strain_elastic[z] = RVE_strain_elastic[z] + (sum_strain_elastic/g)
			RVE_strain_plastic[z] = RVE_strain_plastic[z] + (sum_strain_plastic/g)

		file.write('\n')

		print ('...done\n')
		
	file.write('RVE_STRESS:')
	
	print ('Writing data for RVE')
	
	
	i = 0
	for i in range(len(frameno1)):
	
		file.write(' ' + str(RVE_stress[i]))
	
	i = 0
	file.write(' ')
	
	for i in range(len(frameno2)):
	
		z = i + len(frameno1)
		file.write(' ' + str(RVE_stress[z]))
	i = 0
	file.write('\n')
	file.write('RVE_STRAIN_elastic')
	
	for i in range(len(frameno1)):
	
		file.write(' ' + str(RVE_strain_elastic[i]))
	
	i = 0
	file.write(' ')
	
	for i in range(len(frameno2)):
	
		z = i + len(frameno1)
		file.write(' ' + str(RVE_strain_elastic[z]))

		
	i = 0
	file.write('\n')
	file.write('RVE_STRAIN_plastic:')
	
	for i in range(len(frameno1)):
	
		file.write(' ' + str(RVE_strain_plastic[i]))
	
	i = 0
	file.write(' ')
	
	for i in range(len(frameno2)):
	
		z = i + len(frameno1)
		file.write(' ' + str(RVE_strain_plastic[z]))

	print ('...done\n')

			

	file.close()
	
	odb.close()
	
	#for ref 
	
	
	
if __name__ == '__main__':
	
	function()	
