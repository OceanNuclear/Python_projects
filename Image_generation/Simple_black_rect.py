#!/home/oceanw/anaconda3/bin/python3
# coding: utf-8
from PIL import Image
pixels = ((255,255,255,255),)*5+((255,255,255,100),)*2+((255,255,255,0),)*3
img = Image.new('RGBA', (2,5))
img.putdata(pixels)
img.save('new_rect.png','PNG')
