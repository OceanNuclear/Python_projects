#!/home/oceanw/anaconda3/bin/python3
	#Prepend the code with this line: 
	#(that's where my python environment is)

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
#^This loop will automatically terminate when IndexError is reached. Woohoo!

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

'''To save on iPython'''
get_ipython().magic('save FNF_erf_func 32 33 47 54-58 60')
