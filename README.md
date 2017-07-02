# affineVOTbBox
Ground Truth Affine Transformations for the VOT 2016 Challenge

Repository contains ground truth affine transformation matrices for the [VOT2016](http://www.votchallenge.net/vot2016/dataset.html) Challenge bounding boxes. The transformations are to be used with normalized coordinates (on the interval [-1, 1]).

## Code
The code used to produce the transformations matrices from the original dataset can be found in [transformVot.py](https://github.com/ZigaSajovic/affineVOTbBox/blob/master/transformVOT.py).

### Transform your own dataSet
To transform your own dataSet, it is to be formated like VOT is, ie. the script expects:
* root contains ```list.txt``` listing the relevant directories
* each directory contains ```groundtruth.txt```, where each line represents a bounding box
	* expected line format: ```x1,y1,x2,y2,x3,y3,x4,y4```



```python
python3 transformVOT.py [-i VOTsetPath] [-o outputDirectoryPath]
```
### Example of affine bounding box sampling

![exampleImage](https://github.com/ZigaSajovic/affineVOTbBox/blob/master/example.png)

The code used to produce the image can be found in [exampleTransformation.py](https://github.com/ZigaSajovic/affineVOTbBox/blob/master/exampleTransformation.py).

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">affineVOTbBox</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://si.linkedin.com/in/zigasajovic" property="cc:attributionName" rel="cc:attributionURL">Žiga Sajovic</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.