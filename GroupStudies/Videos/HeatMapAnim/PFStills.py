#!/home/oceanw/anaconda3/bin/python3
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def invertColor(Pic):
	invertedPic = 255*np.ones_like(Pic, dtype= 'uint8') - Pic
	return invertedPic

def addTwoPics(Pic1, Pic2):
	Pic1 = invertedPic(Pic1)
	Pic2 = invertedPic(Pic2)
	sumPic = np.array(Pic1, dtype = 'uint16') + np.array(Pic2, dtype='uint16') #add them up as uint16
	sumPic = [ x-x%255 for x in sumPic]
	sumPic = np.array(sumPic, dtype='uint8')
	return sumPic

def switchColor(Pic):
	return

def modifyPic (Pic):
	return finishedPic

color = 3
fig = plt.figure(frameon=False)
fig.set_size_inches( 21.44,6.71 )

#fig.set_tight_layout(True)
ax = plt.Axes(fig, [0,0,1,1])
fig.add_axes(ax)

ax.set_axis_bgcolor((0, 0, 0))
#ax.set_aspect(671/2144)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame

textBG= 'w'
text = "teststring"
font = ImageFont.truetype('Arial.ttf', 8)
w, h = getSize(text, font)
img = Image.new('RGB', (w+1, h+1), textBG)
d = ImageDraw.Draw(img)
d.text((2,h/2), text, fill='b', font = 'Arial.ttf')
d.rectangle((0,0,w+0.5,h+0.5))

''''
ims = []

for i in range(1):
	inFile = str('{0:0=3}'.format(i+1))+'Frame.png' 
	method = Image.open(inFile)
	
	print("adding Grain",i+1)
	Frame = np.array(method.getdata(), dtype = 'uint8').reshape([method.height, method.width, len(method.getbands())])
	im = plt.imshow(Frame, animated=True)
	if im.get_size()!=(671, 2144) :print("shape if grain",i+1," 's photo is",im.get_size())

	ims.append([im]) #append the method thingy onto the list! I find that weird.

#anim = ax.imshow(fig, ims)
'''
img.save('TestText.png')

