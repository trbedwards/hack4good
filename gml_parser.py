import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from xml.dom import minidom
from shapely.geometry.polygon import Polygon
from postcodes import PostCoder

# reads gml file and returns a dom object
def read_gml(file='data/test4.gml'):
	return minidom.parse(file)

# extract boundaries from list of buildings
def extractBoundaries(buildings):
	# bxy = np.zeros([len(buildings),2])
	coordinates = []
	for ind,building in enumerate(buildings):
		coordinates.append(extractValue(building,'gml:posList').split())
		# bxy[ind] = calcCentre(verts)
	coordinates = flattenList(coordinates)
	num_pairs = len(coordinates)/2
	verts = np.array(coordinates,dtype=float).reshape(num_pairs,2)
	xmin = min(verts[:,0])
	xmax = max(verts[:,0])
	ymin = min(verts[:,1])
	ymax = max(verts[:,1])
	return xmin,ymin,xmax,ymax	

# extract boundaries from gml file
def extractBoundariesGml(gmldoc):
	xmin,ymin = map(float,extractValue(gmldoc,'gml:lowerCorner').split())
	xmax,ymax = map(float,extractValue(gmldoc,'gml:upperCorner').split())
	return xmin,ymin,xmax,ymax	

# calculates the centre of a polygon
def calcCentre(verts):
	xmax = max(verts[:,0])	
	xmin = min(verts[:,0])	
	ymax = max(verts[:,1])
	ymin = min(verts[:,1])
	xc = (xmax+xmin)/2
	yc = (ymax+ymin)/2
	return xc,yc

# calculate area of polygon

def flattenList(list):
	return [item for sublist in list for item in sublist]

def extractValue(doc,tagname):
	return doc.getElementsByTagName(tagname)[0].firstChild.nodeValue

def extractElements(gmldoc,tagname='vmd:Building'):
	return gmldoc.getElementsByTagName(tagname)

def calcBuildingArea(building):
	return calcMultiArea(building,'gml:exterior') - calcMultiArea(building,'gml:interior')	

def calcMultiArea(building,elementName):
	elements = extractElements(building,elementName)
	area = 0
	# area = reduce(lambda x,y:x+y, [calcArea(extractCoordinates(e)) for e in elements])
	for e in elements:
		coordinates = extractCoordinates(e)
		area += calcArea(coordinates) 
	return area

def calcArea(coordinates):
	pairs = []
	for i in xrange(len(coordinates)/2):
		pairs.append(map(float,(coordinates[i*2], coordinates[i*2+1])))
	polygon = Polygon(pairs)
	return polygon.area

def extractCoordinates(obj):
	return extractValue(obj,'gml:posList').split()

def createFigure(buildings,boundaries=None):

	# extract boundaries
	if not boundaries:
		boundaries = extractBoundaries(buildings)

	# setup figure
	fig = plt.figure()
	ax = fig.add_subplot(111)
	xmin,ymin,xmax,ymax = boundaries
	ax.set_xlim(xmin,xmax)
	ax.set_ylim(ymin,ymax)

	# loop over buildings
	for building in buildings:

		# color of building
		fcolor = (0.5,0.5,0.5) # RGB

		# extract list of coordinates for building
		coordinates = extractValue(building,'gml:posList').split()
		num_pairs = len(coordinates)/2

		# load coordinates into vertices array
		verts = np.array(coordinates,dtype=float).reshape(num_pairs,2)

		# create polygon path
		codes = np.array([Path.MOVETO]+[Path.LINETO]*(num_pairs-2)+[Path.CLOSEPOLY])
		path = Path(verts, codes)

		# add polygon to figure 
		patch = patches.PathPatch(path, facecolor=fcolor, lw=0)
		ax.add_patch(patch)

	plt.show()

def loadBuildings(gmlfile,tagname='vmd:Building'):
	gmldoc = read_gml(gmlfile)
	return gmldoc,extractElements(gmldoc,tagname=tagname)

def calcDists(pxy,buildingsPos):
	distances = np.zeros(len(buildingsPos)) 
	i = 0
	for bxy in buildingsPos:
		distances[i] = calcDist(pxy,bxy)
		i+=1
	return distances

def calcDist(u,v):
	dx = u[0]-v[0]
	dy = u[1]-v[1]
	return dx*dx + dy*dy 

def locationOfPostcode(postcode):
	pc = PostCoder()
	result = pc.get(postcode)
	x = result['geo']['easting']
	y = result['geo']['northing']
	return x,y

def locationOfBuilding(building):
	coordinates = extractValue(building,'gml:posList').split()	
	verts = np.array(coordinates,dtype=float).reshape(len(coordinates)/2,2)
	return calcCentre(verts)

def appendObject(doc,parent,tag,value):
	child = createObject(doc,tag,value)
	parent.appendChild(child)

def createObject(doc,tag,value):
	obj = doc.createElement(tag)
	txt = doc.createTextNode(value)
	obj.appendChild(txt)
	return obj

def replaceFeatures(gmldoc,newFeatures):
	oldFeatures = extractElements(gmldoc,'vmd:featureMember')
	featureCollection = extractElements(gmldoc,'vmd:featureCollection')
	for feature in oldFeatures:
		featureCollection.removeChild(feature)
	for feature in newFeatures:
		featureCollection.appendChild(feature)

def createNewGml(fileName,buildings):
	newDoc = minidom.Document()
	featureCollection = newDoc.createElement('vmd:FeatureCollection')
	for building in buildings:
		feature = newDoc.createElement('vmd:featureMember')
		feature.appendChild(building)
		featureCollection.appendChild(feature)
	newDoc.appendChild(featureCollection)
	writeGml2file(fileName,newDoc)

def writeGml2file(fileName,doc,flag='w'):
	with open(fileName, flag) as f:
		doc.writexml(f)
		f.close()
