from maps import getTransMat, bBoxWithContext, bBoxReorient
from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image
from argparse import ArgumentParser
import numpy as np
 
parser = ArgumentParser(description="A script for working with boundingBox dataSets.")
parser.add_argument("-i","--sourceDir",dest="inDir",action="store", metavar="DIRECTORY", default="./",\
     help="Directory of VOT set")
parser.add_argument("-d", "--destinationDir", dest="outDir", action="store", metavar="DIRECTORY", default="./", \
     help="Directory for output file set")
parser.add_argument("-c", "--addContext", dest="context", action="store", metavar="CONTEXT FACTOR",\
     help="Scaling factor for the bBox, used to add context")
parser.add_argument("-r", "--reorient", dest="reOr", action="store_true", default=False, \
     help="Reorient the boundingBoxes to have consistent orientation through time.")
parser.add_argument("-a", "--affine", dest="affine", action="store_true", default=True, \
     help="Produce the matrix for affine transformation into the boundingBox.")
args = parser.parse_args()
pathVOT=args.inDir
pathOut=args.outDir
reOrient=args.reOr
context=args.context
affine=args.affine
if context is not None:
 context=float(context)
 assert context>=1, "Context factor [-c] should be larger or equal to one (1)."
imgFormats=["jpg","png"]
groundTruth="groundtruth.txt"
groundTruthOut="groundtruthAffine.txt"
groundTruthOutContext="groundtruthAffineWithContext.txt"
groundTruthReoriented="groundtruthReoriented.txt"
groundTruthReorientedContext="groundtruthReorientedWithContext.txt"
groundTruthContex="groundtruthWithContext.txt"
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
   bBoxesReoriented=bBoxReorient(np.loadtxt(join(path,groundTruth),delimiter=","))
   with open(join(pathOutTemp,groundTruthReoriented),'w') as reorientedOut:
   	for bBox in bBoxesReoriented:
   	 print(','.join(str(s) for s in bBox),file=reorientedOut)
   bBoxPath=join(pathOutTemp,groundTruthReoriented)
   groundTruthContext=groundTruthReorientedContext
  else:
   bBoxPath=join(path,groundTruth)
  imgs=[f for f in listdir(path) if isfile(join(path, f))]
  imgs.sort()
  with open(bBoxPath) as bBoxes:
   f = open(join(pathOutTemp,groundTruthOut),'w') if affine else False
   f2 =open(join(pathOutTemp,groundTruthContext),'w') if context is not None else False
   f3 =open(join(pathOutTemp,groundTruthOutContext),'w') if affine and context is not None else False
   files_=[f,f2,f3]
   for im,bBox in zip(imgs,bBoxes):
    with Image.open(join(path,im)) as IMG:
     width, height = IMG.size
     box=[float(p) for p in bBox.split(",")]
     if affine:
      trans=getTransMat(box,(height,width))
      print(','.join(str(s) for s in trans.flatten()),file=f)
     if context is not None:
      boxC=bBoxWithContext(box,(height,width), context)
      print(','.join(str(s) for s in boxC.reshape(-1)), file=f2)
      if affine:
       trans=getTransMat(boxC,(height,width))
       print(','.join(str(s) for s in trans.flatten()),file=f3)
   for f_ in files_:
    if f_:
     f_.close()
  print(dir.strip(),file=listOut)
  print("Finished processing directory %s" % dir.strip())