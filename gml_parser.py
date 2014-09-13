import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from xml.dom import minidom

# reads gml file and returns a dom object
def read_gml(file='data/test4.gml'):
	return minidom.parse(file)

# extract buildings
def extractBuildings(gmldoc):
	buildings = gmldoc.getElementsByTagName('vmd:Building')
	return buildings

# extract boundaries from list of buildings
def extractBoundaries(buildings):
	bxy = np.zeros([len(buildings),2])
	for ind,building in enumerate(buildings):
		coordinates = extractValue(building,'gml:posList').split()
		num_pairs = len(coordinates)/2
		verts = np.array(coordinates,dtype=float).reshape(num_pairs,2)
		bxy[ind] = calcCentre(verts)
	xmin = min(bxy[:,0])
	xmax = max(bxy[:,0])
	ymin = min(bxy[:,1])
	ymax = max(bxy[:,1])
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

# returns the value from the element with specified tagname
def extractValue(doc,tagname):
	return doc.getElementsByTagName(tagname)[0].firstChild.nodeValue

# create figure
def createFigure(buildings,boundaries):

	# setup figure
	fig = plt.figure()
	ax = fig.add_subplot(111)
	xmin,ymin,xmax,ymax = boundaries
	ax.set_xlim(xmin,xmax)
	ax.set_ylim(ymin,ymax)

	# loop over buildings
	for building in buildings:

		# color of building
		fcolor = (1,1,1) # RGB

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