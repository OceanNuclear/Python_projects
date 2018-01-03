#!/home/oceanw/anaconda3/bin/python3
#This program extract two particular character from each line of a txt input file and then print them out
import numpy as np
import matplotlib.pyplot as plt

Chosen = [0,4,8,11]
Min=0
Max=1

Count = [np.zeros(8192),]*(12)
inFile = ["",]*(12)
plot = ["",]*12	
t = []
for spectrum in Chosen:
	inFile[spectrum] = str("Unknown-Sample-09-10min-"+'{:0=3.0f}'.format( spectrum )+".Spe")
	numLines = sum(1 for line in open(inFile[spectrum]))
	f = open(inFile[spectrum], "r")
	f.seek(193)

	#save data
	for channel in range (8192):
		Count[spectrum][channel] = int(f.readline())
	
	#plot
	t = str( '{:0=3.0f}'.format( spectrum*10 ) +" to "+ '{:0=3.0f}'.format( spectrum*10 +10 )+ " minutes")
	plt.semilogy(Count[spectrum], label = t)
	#t.append ( str( '{:0=3.0f}'.format( spectrum*10 ) +" to "+ '{:0=3.0f}'.format( spectrum*10 +10 )+ " minutes") )
plt.legend() #Aarh yes I'm so happy finally got it working without having to use a handler!
plt.xlabel("Channel number")
plt.ylabel("Counts")
plt.show()
