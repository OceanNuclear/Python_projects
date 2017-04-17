#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
from PIL import Image

#img = Image.new('RGB', (2,5))
#Define a single transparent/green pixle
trans = (255,255,255,0)
green = (0, 255, 0, 255)
xdiv = 10
ydiv = 10
xthick = 6
ythick = 6
xdim = 1600
ydim = 1200
bWidth = int(xdim/xdiv)
bHeight = int(ydim/ydiv)


#Template half/full columns
midBlock = (trans,)*(bWidth-xthick)+ (green,)*xthick
#midBlock is now 160 pixels long
midBlock = midBlock*(xdiv-1)
#midBlock is now 1440 pixels long
Row = (trans,)*(int(bWidth/2)-xthick)+ (green,)*xthick+ midBlock+ (trans,)*int(bWidth/2)
#Row is now exactly 1 row of pixels long (1600 pixels)
row = Row*xthick

midCo = (trans,)*(bHeight-ythick)*xdim+ row
midCo = midCo * (ydiv-1)

fullPic = (trans,)*(int(bHeight/2)-ythick)*xdim +row + midCo+ (trans,)*int(bHeight/2)*xdim

img3 = Image.new('RGBA', (1600,1200))
img3.putdata(fullPic)
img3.save('FNF_array.png', 'PNG')
