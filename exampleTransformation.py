import matplotlib.pyplot as plt
from maps import sampleGrid
from scipy import misc
import numpy as np

"""
This example works with the first image
from the directory bag of the VOT dataset
transformation matrix can be found as the first
line in the bag/groundtruthAffine.txt
"""

trans=np.array\
	([0.21701,-0.0870729,0.521698,0.167833,0.200139,0.0810833,0.0,0.0,1.0]).reshape((3,3))
Im=misc.imread("exampleBag.jpg")
bBox1=sampleGrid(trans, Im, (80,80))
bBox2=sampleGrid(trans, Im, (60,104))
plt.figure()
gs=plt.GridSpec(2,2)
ax1=plt.subplot(gs[0,:])
ax2=plt.subplot(gs[1,0])
ax3=plt.subplot(gs[1,1])
ax1.set_title("Original",fontsize=16)
ax2.set_title("80 by 80 Affine Sampling of Bounding Box",fontsize=16)
ax3.set_title("60 by 104 Affine Sampling of Bounding Box",fontsize=16)
for i, ax in enumerate(plt.gcf().axes):
 for tl in ax.get_xticklabels() + ax.get_yticklabels():
  tl.set_visible(False)
ax1.imshow(Im)
ax2.imshow(bBox1)
ax3.imshow(bBox2)
plt.show()