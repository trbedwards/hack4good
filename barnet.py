from gml_parser import *
from PVcalc import *
import matplotlib.pyplot as plt
from utils import write2csv

def readCsv(file,header=True):
	with open(file,'r') as f:
		lines = f.readlines()
	if header:
		lines.pop(0)
	return np.array([line.strip().split(',') for line in lines])

def calculatePV(building):
	PV = PVcalc()
	PV.loadBuilding(building)
	PV.setUpPVcalc()
	PV.calcMoneySaved()
	PV.calcCost()
	PV.calcTimeForBreakEven()
	return PV.M,PV.cost,PV.t

def newCsv(file):
	with open(file,'w') as f:
		f.close()

def readPostcodes(data):
	return [i[1] for i in data]

def plotPostcodes(postcodes):
	points = []
	for postcode in postcodes:
		pxy = locationOfPostcode(postcode)
		points.append(pxy)
	scatterPlot(points)

def plotBuildingsPos(buildings):
	points = []
	for building in buildings:
		bxy = locationOfBuilding(building)
		points.append(bxy)
	scatterPlot(points)

def plotPostcodesAndBuildings(postcodes,buildings):
	ppoints = []
	for postcode in postcodes:
		pxy = locationOfPostcode(postcode)
		ppoints.append(pxy)
	bpoints = []
	for building in buildings:
		bxy = locationOfBuilding(building)
		bpoints.append(bxy)

	scatterPlotBoth(ppoints,bpoints)

def scatterPlot(points):
	# fig,ax = setupFigure()
	x = [i[0] for i in points]
	y = [i[1] for i in points]
	plt.scatter(x,y)
	plt.show()

def scatterPlotBoth(ppoints,bpoints):
	px = [i[0] for i in ppoints]
	py = [i[1] for i in ppoints]
	bx = [i[0] for i in bpoints]
	by = [i[1] for i in bpoints]
	fig,ax = setupFigure()
	ax.scatter(px,py,c='y',label='Postcodes')
	ax.scatter(bx,by,c='r',label='Buildings')
	plt.legend(loc='upper left')
	plt.show()

def setupFigure():
	fig = plt.figure()
	ax = fig.add_subplot(111)
	return fig,ax

def calcPostcodeDists(postcode,buildings):
	distances = np.zeros(len(buildings)) 
	pxy = locationOfPostcode(postcode)

	i = 0
	for b in buildings:
		bxy = locationOfBuilding(b)
		distances[i] = calcDist(pxy,bxy)
		i+=1

	return distances

if __name__ == "__main__":

	data = readCsv('data/barnet_all.csv')
	postcodes = readPostcodes(data)
	# postcodes = postcodes[0:8]
	print "loading buildings..."
	gmldoc,buildings = loadBuildings('data/TQ28.gml')
	# buildings = loadBuildings('data/barnet8.gml')
	newCsv('data/barnet_all_PV.csv')

	for i,postcode in enumerate(postcodes):

		print i,postcode

		distances = calcDists(postcode,buildings) 
		closestIndex = np.argmin(distances)
		# print "closest index = ", closestIndex
		# print distances
		closestBuilding = buildings[np.argmin(distances)]
		buildingPos = locationOfBuilding(closestBuilding)
		savings, cost, years = calculatePV(closestBuilding)
		write2csv((postcode,buildingPos[0],buildingPos[1],savings,cost,years),'data/barnet_all_PV.csv')
		print savings,cost,years
		print ""
