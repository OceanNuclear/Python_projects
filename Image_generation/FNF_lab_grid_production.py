#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
from PIL import Image

#This python code is written for the purpose of generating a transparent
# .png grid to overlay onto any metallurgy micrograph, so that phase-
# counting can be done.
#Sharable under the MIT license.
#-Ocean Wong, April 2017

#img = Image.new('RGB', (2,5))
#Define a single transparent/green pixle
trans = (255,255,255,0)
green = (0, 255, 0, 255)
#Define the number of division/thickness of each dot/dimension in x/y direction.
xdiv = 10
ydiv = 10
xthick = 4
ythick = 4
xdim = 800
ydim = 600
bWidth = int(xdim/xdiv)
bHeight = int(ydim/ydiv)


#Template half/full columns
midBlock = (trans,)*(bWidth-xthick)+ (green,)*xthick
#midBlock is now 160 pixels long
midBlock = midBlock*(xdiv-1)
#midBlock is now 1440 pixels long
Row = (trans,)*(int(bWidth/2)-xthick)+ (green,)*xthick+ midBlock+ (trans,)*int(bWidth/2)
#Row is now exactly 1 row of pixels long (1600 pixels)
row = Row*ythick

#Make a variable called mid-Co so that it takes up 9 "full columns" in the middle of the picture.
midCo = (trans,)*(bHeight-ythick)*xdim+ row
midCo = midCo * (ydiv-1)

#Generate the full picture
fullPic = (trans,)*(int(bHeight/2)-ythick)*xdim +row + midCo+ (trans,)*int(bHeight/2)*xdim

#Output
img3 = Image.new('RGBA', (xdim,ydim))
img3.putdata(fullPic)
img3.save('FNF_array2.png', 'PNG')
