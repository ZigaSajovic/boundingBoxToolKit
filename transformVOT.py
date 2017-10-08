from maps import getTransMat
from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image
from argparse import ArgumentParser
import numpy as np
from itertools import permutations

def reorient(pathOr, pathOut):
 bBoxes=np.loadtxt(pathOr,delimiter=",")
 l = list(permutations(range(4)))
 with open(pathOut,'w') as out:
  print(','.join(str(s) for s in bBoxes[0].flatten()),file=out)
  a1=bBoxes[0].reshape((4,2))
  for i in range(1,bBoxes.shape[0]):
   a2=bBoxes[i].reshape((4,2))
   min_=None
   mm=None
   for L in l:
    a2_=np.take(a2,L, axis=0)
    sm=((a1-a2_)**2).sum()
    if min_ is None or sm < min_:
     min_=sm
     mm=a2_
   a1=mm
   print(','.join(str(s) for s in mm.reshape(-1)),file=out)

parser = ArgumentParser()
parser.add_argument("-i","--sourceDir",dest="inDir",action="store", metavar="DIRECTORY", default="./",\
					help="Directory of VOT set")
parser.add_argument("-o", "--destinationDir", dest="outDir", action="store", metavar="DIRECTORY", default="./", \
					help="Directory for output file set")
parser.add_argument("-r", "--reorient", dest="reOr", action="store_true", default=False, \
					help="Should it reorient the boundingBoxes")
args = parser.parse_args()
pathVOT=args.inDir
pathOut=args.outDir
reOrient=args.reOr
imgFormats=["jpg","png"]
groundTruth="groundtruth.txt"
groundTruthOut="groundtruthAffine.txt"
groundTruthReoriented="groundtruthReoriented.txt"
if not exists(pathOut):
	makedirs(pathOut)
with open(join(pathVOT,"list.txt"),'r') as list_, \
		open(join(pathOut, "list.txt"), 'w') as listOut:
	for dir in list_:
		print("Start processing directory %s"%dir.strip())
		path=join(pathVOT,dir.strip())
		pathOutTemp = join(pathOut, dir.strip())
		if not exists(pathOutTemp):
			makedirs(pathOutTemp)
		if reOrient:
			reorient(join(path,groundTruth),join(pathOutTemp,groundTruthReoriented))
			bBoxPath=join(pathOutTemp,groundTruthReoriented)
		else:
			bBoxPath=join(path,groundTruth)
		imgs=[f for f in listdir(path) if isfile(join(path, f))]
		imgs.sort()
		with open(bBoxPath) as bBoxes,\
			open(join(pathOutTemp,groundTruthOut),'w') as f:
			for im,bBox in zip(imgs,bBoxes):
				with Image.open(join(path,im)) as IMG:
					width, height = IMG.size
					box=[float(p) for p in bBox.split(",")]
					trans=getTransMat(box,(height,width))
					print(','.join(str(s) for s in trans.flatten()),file=f)
		print(dir.strip(),file=listOut)
		print("Finished processing directory %s" % dir.strip())