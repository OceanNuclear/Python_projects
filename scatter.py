#!/home/oceanw/anaconda3/bin/python
# -*- coding: utf-8 -*-
#
#  scatter.py
#  
#  Copyright 2016 Ocean <oceanw@oceanw-HP-Stream-Notebook-PC-11>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


def main(args):
    return 0
#don't konw why but it failed
if __name__ == '__main__':
	import sys
	import matplotlib

M=input ("What is the mass of the cube?(in kg)")
m_dot=input ("What is the mass flow rate of the propellant?(in kg/s)")
Vg=input ("What is the speed at which the propellant is ejected?(in m/s)")
R=input("What is the side length of the cube?(in m)")
c= 1/6 # coefficient for moment of inertia for a cube
u= math.sqrt(2*c*R*m_dot*Vg/m) #the constant used to simplify the integration


from pylab import *

x = [0,2,-3,-1.5]
y = [0,3,1,-2.5]
color=['m','g','r','b']

scatter(x,y, s=100 ,marker='o', c=color)

show()

sys.exit(main(sys.argv))
