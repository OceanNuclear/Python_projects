#!/home/oceanw/anaconda3/bin/python

import fmod
N = int(input("N = "))

import numpy as np
w = np.zeros(N, 'd')
print(type(w))
fmod.func(w)
#Quite sure that this is 
#modulename.subroutinename(N)
print(type(w))
print(w)

#f2py -c filename.f -m modulename
#i.e.
#f2py -c forty.f -m fmod
#https://docs.scipy.org/doc/numpy-dev/f2py/getting-started.html
#YES IT WORKS!
