import maps
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

A=np.loadtxt("/bag/groundtruthAffine.txt",delimiter=',')
B=np.loadtxt("/groundtruthReoriented.txt",delimiter=',')

fig = plt.figure()

gs=plt.GridSpec(3,3)
ax1=plt.subplot(gs[:,0:2])
ax2=plt.subplot(gs[1,2])
line=plt.Polygon(B[0].reshape((4,2)), fill=None, closed=True)
ax1.set_title("boundingBox",fontsize=16)
ax2.set_title("affine sample",fontsize=16)
def init():
 a=mpimg.imread("../vot2016/bag/%08d.jpg"%1)
 ax1.imshow(a)
 ax1.add_line(line)

def update(i):
	a=mpimg.imread("/home/ziga/Downloads/vot2016/bag/%08d.jpg"%i)
	ax1.imshow(a)
	ax2.imshow(maps.sampleGrid(A[i-1].reshape((3,3)), a, (40,60)))
	line.set_xy(B[i-1].reshape((4,2)))
anim = FuncAnimation(fig, update, init_func=init, frames=np.arange(1, A.shape[0]), interval=200)

for i, ax in enumerate(plt.gcf().axes):
	ax.axis('off')
#anim.save('animation.gif', fps=30, extra_args=['-vcodec', 'h264', '-pix_fmt', 'yuv420p'])
anim.save('animation3.gif', dpi=80, writer='imagemagick')
plt.show()
