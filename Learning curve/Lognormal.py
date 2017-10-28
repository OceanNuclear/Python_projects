#!/home/oceanw/anaconda3/bin/python3
#Code for generating a lognormal distribution, for purely testing purpose.
#Unfinished.

# coding: utf-8
def Reset_x( mu , sigma ):
    x = [0 for x in range (15)]
    x[0] = rn.lognormvariate( mu , sigma )
    for i in range( 1 , 15 ):
        x[i] = x[i-1] + rn.lognormvariate( mu , sigma ) - 0.05
        if x [i] > 1:
            x[i] = 1
    return x
	print(x)
