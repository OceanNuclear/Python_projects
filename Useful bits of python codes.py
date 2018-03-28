#!/home/oceanw/anaconda3/bin/python3
	#Prepend the code with this line: 
	#(that's where my python environment is)
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi

def removeBrackets(array):
	if np.shape(array)==():
		print(array, "is EMPTY!")
	while ( ( np.shape(array)[0]==1 ) & ( np.ndim(array)>1 ) ):
		array = array[0]
	return array

'''In terminal, type '''
chmod +x code.py
./code.py

'''input loops'''
Tinput = str(input("Temperature T of the system (in keV or K) is: "))
item = splitted(Tinput)
print(item)
T_u = str(item[1])
T = float(item[0])
if (T_u!="eV") and (T_u!="K"):
	print("Invalid unit! Exiting...")
	exit()
elif (T_u == "eV"):
	k_T = c.e*T
elif (T_u == "K"):
	k_T = c.k*T

'''try for loop'''
try:
	for i in range (0,100000):
		y.append(x[i]) #or do anything else
except IndexError:
	pass
#^This loop will automatically terminate when we run out of x to append. Woohoo!

'''To read from file:'''
f = open(Infile, "r")
f.seek(-1,1) #f.seek(offset, from_what), where from_what = 0 for start of file, =1 for current position, =2 for end of file.
f.read(4) #etc.
	#side note this is a beautiful way of counting the number of lines
n_data = sum(1 for line in open(Infile))

#To prompt user input:
Infile = str(input("What's the data's file name?\n"))

'''definition of lists/tuple'''
#[, , ] OR [[],[] ,[] ] OR [(),(),()] makes a list
#(, , ) makes a tuple, so on and so forth
x = np.zeros(shape=(5,2))

#For ipython:
%save FNF_erf_func.py 32 33 47 54-58 60
ctrl+s can be unfrozen by ctrl+q
ctrl+r for reverse search
