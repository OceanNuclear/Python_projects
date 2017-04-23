#Prepend the code with this line: 
'#!/home/oceanw/anaconda3/bin/python3'
(that's my development environment)

#In terminal, type 
'chmod +x code.py'
'./code.py'

#try for loop
try:
	for i in range (0,100000):
		y.append(x[i]) #or do anything else
except IndexError:
	pass
#^This loop will automatically terminate when IndexError is reached. Woohoo!

#To read from file:
f = open(Infile, "r")
f.seek(-1,1) #f.seek(offset, from_what), where from_what = 0 for start of file, =1 for current position, =2 for end of file.
f.read(4) #etc.
	#side note this is a beautiful way of counting the number of lines
n_data = sum(1 for line in open(Infile))

#To prompt user input:
Infile = str(input("What's the data's file name?\n"))

#[, , ] OR [[],[] ,[] ] OR [(),(),()] makes a list
#(, , ) makes a tuple, so on and so forth
