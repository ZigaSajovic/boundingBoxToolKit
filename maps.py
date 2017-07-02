import numpy as np
import scipy

def transformationMatrix(imXs, bBXs):
	ptsN = len(imXs)
	X, Y, U, V, O, I = imXs[:, 0], imXs[:, 1], bBXs[:, 0], bBXs[:, 1], np.zeros([ptsN]), np.ones([ptsN])
	A = np.concatenate((np.stack([X, Y, I, O, O, O], axis=1),
						np.stack([O, O, O, X, Y, I], axis=1)), axis=0)
	b = np.concatenate((U, V), axis=0)
	p = scipy.linalg.lstsq(A, b)[0].squeeze()
	return np.array([[p[0], p[1], p[2]], [p[3], p[4], p[5]], [0, 0, 1]], dtype=np.float32)

def normalizeBbox(bBox, shape):
	nBbox=np.array(bBox)/(shape[1],shape[0])-1
	return nBbox

def getTransMat(bBox, shape):
	box=normalizeBbox(np.array(bBox).reshape((4,2)),shape)
	toMap=np.array([-1,-1,1,-1,1,1,-1,1]).reshape((4,2))
	return transformationMatrix(toMap,box)

def sampleGrid(transformation, img, shapeOut):
	shape=img.shape
	x,y = np.meshgrid(np.linspace(-1, 1, shapeOut[1]), np.linspace(-1, 1, shapeOut[0]))
	xt=x.flatten()
	yt=y.flatten()
	toMap=np.stack([xt,yt,np.ones_like(xt)],axis=0)
	X,Y,_=transformation.dot(toMap)
	x0=(X+1)*shape[1]
	y0=(Y+1)*shape[0]

	x=x0
	y=y0
	x0=x0.astype(np.int)
	y0=y0.astype(np.int)

	x1=x0+1
	y1=y0+1
	x0,x1=np.clip(np.stack((x0,x1),axis=0),0,shape[1])
	y0, y1 = np.clip(np.stack((y0, y1), axis=0), 0, shape[0])
	idx_a = (y0*shape[1] + x0).astype(np.int)
	idx_b = (y1*shape[1] + x0).astype(np.int)
	idx_c = (y0*shape[1] + x1).astype(np.int)
	idx_d = (y1*shape[1] + x1).astype(np.int)

	wa = np.expand_dims(((x1.astype(np.float) - x) * (y1.astype(np.float) - y)),axis=1)
	wb = np.expand_dims(((x1.astype(np.float) - x) * (y - y0.astype(np.float))),axis=1)
	wc = np.expand_dims(((x - x0.astype(np.float)) * (y1.astype(np.float) - y)),axis=1)
	wd = np.expand_dims(((x - x0.astype(np.float)) * (y - y0.astype(np.float))),axis=1)

	im_flat=img.reshape((-1,shape[2]))
	Ia = im_flat[idx_a]
	Ib = im_flat[idx_b]
	Ic = im_flat[idx_c]
	Id = im_flat[idx_d]
	return (wa * Ia+ wb * Ib+ wc * Ic+ wd * Id).reshape(shapeOut+(shape[2],)).astype(np.uint8)