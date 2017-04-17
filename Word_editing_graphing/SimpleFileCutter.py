#!/home/oceanw/anaconda3/bin/python3
Infile = str(input("Please type in the input filename:\n"))
Outfile = str(input("Please type in the output filename:\n"))
numlines = sum(1 for line in open(Infile))
f = open(Infile, "r")
o = open(Outfile, "w")
#opened a file and ready to read from it.
s=["" for x in range (numlines)]
for n in range (numlines):
	s[n]=(str(f.readline()))
	#stored each line of text, will examine them character by character.
	x = len(s[n])
	score = str(s[n][x-4])+str(s[n][x-3])
	o.write(score)
	o.write('\n')
f.seek(0)
f.close()
o.close()
int 
