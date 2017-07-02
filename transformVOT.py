from maps import getTransMat
from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i","--sourceDir",dest="inDir",action="store", metavar="DIRECTORY", default="./",\
					help="Directory of VOT set")
parser.add_argument("-o", "--destinationDir", dest="outDir", action="store", metavar="DIRECTORY", default="./", \
					help="Directory for output file set")
args = parser.parse_args()
pathVOT=args.inDir
pathOut=args.outDir
imgFormats=["jpg","png"]
groundTruth="groundtruth.txt"
groundTruthOut="groundtruthAffine.txt"
if not exists(pathOut):
	makedirs(pathOut)
with open(join(pathVOT,"list.txt"),'r') as list, \
		open(join(pathOut, "list.txt"), 'w') as listOut:
	for dir in list:
		path=join(pathVOT,dir.strip())
		pathOutTemp = join(pathOut, dir.strip())
		if not exists(pathOutTemp):
			makedirs(pathOutTemp)
		imgs=[f for f in listdir(path) if isfile(join(path, f))]
		imgs.sort()
		print("Start processing directory %s"%dir.strip())
		with open(join(path,groundTruth)) as bBoxes,\
			open(join(pathOutTemp,groundTruthOut),'w') as f:
			for im,bBox in zip(imgs,bBoxes):
				with Image.open(join(path,im)) as IMG:
					width, height = IMG.size
					box=[float(p) for p in bBox.split(",")]
					trans=getTransMat(box,(height,width))
					print(','.join(str(s) for s in trans.flatten()),file=f)
		print(dir.strip(),file=listOut)
		print("Finished processing directory %s" % dir.strip())