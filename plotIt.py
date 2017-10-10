import matplotlib.pyplot as plt
import numpy as np

A=np.loadtxt("/home/ziga/affineVOTbBox/bag/groundtruthReoriented.txt",delimiter=',')

A=np.loadtxt("/home/ziga/Downloads/vot2016/bag/groundtruth.txt",delimiter=',')


# from itertools import permutations
# a1=A[1].reshape((4,2))
# a2=A[2].reshape((4,2))
# min_=None
# mm=None
# for L in l:
#  a2_=np.take(a2,L, axis=0)
#  sm=((a1-a2_)**2).sum()
#  if min_ is None or sm < min_:
#   min_=sm
#   mm=L

A=A.reshape((A.shape[0],4,2))
A=A[0:2]
print(A)
plt.scatter(A[1,:,0],A[1,:,1],color='red', s=500)
plt.scatter(A[0,:,0],A[0,:,1],color='blue', s=500)

for i, S in enumerate(A[0]):
 plt.annotate(
        "vertex "+str(i),
        xy=(S[0], S[1]), xytext=(-20, -20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
for i, S in enumerate(A[1]):
  plt.annotate(
        "vertex "+str(i),
        xy=(S[0], S[1]), xytext=(20, 20),
        textcoords='offset points', ha='left', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
for i, ax in enumerate(plt.gcf().axes):
 for tl in ax.get_xticklabels() + ax.get_yticklabels():
  tl.set_visible(False)

plt.show()