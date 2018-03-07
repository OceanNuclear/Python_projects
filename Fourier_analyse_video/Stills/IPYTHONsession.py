#!/home/oceanw/anaconda3/bin/python3

import matplotlib.pyplot as plt
from PIL import Image

fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0,0,1,1])
ax.set_axis_off()
fig.add_axes(ax)
im = Image.open("00:06_reconstructed.png")
ax.imshow(im, aspect = 'normal')
#plt.plot([],[])
fig.savefig("resaved0006snapshot.png")
