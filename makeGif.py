import maps
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

A=np.loadtxt("/bag/groundtruthAffine.txt",delimiter=',')
B=np.loadtxt("/bag/groundtruthReorientedWithContext.txt",delimiter=',')
A2=np.loadtxt("/bag/groundtruthAffineWithContext.txt",delimiter=',')
C=np.loadtxt("/bag/groundtruthReoriented.txt",delimiter=',')

fig = plt.figure()
gs=plt.GridSpec(2,3)
ax1=plt.subplot(gs[:,0:2])
ax2=plt.subplot(gs[0,2])
ax3=plt.subplot(gs[1,2])
line=plt.Polygon(B[0].reshape((4,2)), color="blue", fill=None, closed=True)
line2=plt.Polygon(C[0].reshape((4,2)),color="red", fill=None, closed=True)

ax1.set_title("boundingBox",fontsize=16)
ax2.set_title("affine sample",fontsize=16)
ax3.set_title("affine sample\n with context",fontsize=16)

def init():
 a=mpimg.imread("/vot2016/bag/%08d.jpg"%1)
 ax1.imshow(a)
 ax1.add_line(line)
 ax1.add_line(line2)

def update(i):
	a=mpimg.imread("/vot2016/bag/%08d.jpg"%i)
	ax1.imshow(a)
	ax2.imshow(maps.sampleGrid(A[i-1].reshape((3,3)), a, (40,60)))
	ax3.imshow(maps.sampleGrid(A2[i-1].reshape((3,3)), a, (40,60)))
	line.set_xy(B[i-1].reshape((4,2)))
	line2.set_xy(C[i-1].reshape((4,2)))
anim = FuncAnimation(fig, update, init_func=init, frames=np.arange(1, A.shape[0]), interval=200)
for i, ax in enumerate(plt.gcf().axes):
	ax.axis('off')

#anim.save('animation.mp4', fps=30, extra_args=['-vcodec', 'h264', '-pix_fmt', 'yuv420p'])
red_patch = mpatches.Patch(color='red', label='The red data')
blue_patch = mpatches.Patch(color='blue', label='The blue data')
fig.legend(handles=[blue_patch,red_patch], labels=["bBox with Context 1.5","boundingBox"], loc="lower center")
#anim.save('animation4.gif', dpi=80, writer='imagemagick')
plt.show()
