import numpy as np
import urllib
import json
from PVcalc import PVcalc
from utils import *
from latlon_to_bng import WGS84toOSGB36
# import utm
from gml_parser import *

def loadSchoolData():
	f = urllib.urlopen("http://www.education.gov.uk/schools/performance/geo/la202_all.html")
	text = f.readlines()
	schDataStr = text[58][8:]
	schDataStrPruned = schDataStr[:-2]
	return json.loads(schDataStrPruned)

def findSchool(schData,schName):
	school = None
	for i in schData:
		if i['name'] == schName:
			school = i
	if school:
		return school
	else:
		print "School '%s' not found" % schName
		return

def findSchoolBuilding(buildings,buildingsPos,schPos,method):
	if method == 'lat_long':
		# utmPos = utm.from_latlon(schPos[0],schPos[1])
		# easting,northing = (utmPos[0],utmPos[1])
		easting,northing = WGS84toOSGB36(schPos[0],schPos[1])
	else:
		easting,northing = (schPos[0],schPos[1])
	return locateBuilding(buildings,buildingsPos,(easting,northing))

def locateBuilding(buildings,buildingsPos,pos):
	distances = calcDists(pos,buildingsPos)
	index = np.argmin(distances)
	print index
	closestBuilding = buildings[np.argmin(distances)]
	return closestBuilding


def loadBuildingsPos(buildings):
	positions = []
	for building in buildings:
		positions.append(locationOfBuilding(building))
	return np.array(positions)

def annotateBuilding(gmldoc,building,schPos,schName):
	posStr = "%s %s" % (schPos[0],schPos[1])
	appendObject(gmldoc,building,'gml:schName',schName)
	appendObject(gmldoc,building,'gml:schPos',posStr)

def calculatePV(building):
	PV = PVcalc()
	PV.loadBuilding(building)
	PV.setUpPVcalc()
	PV.calcMoneySaved()
	PV.calcCost()
	PV.calcTimeForBreakEven()
	return PV.M,PV.cost,PV.t


if __name__ == "__main__":

	print "loading school data..."
	schools = loadSchoolData()['schools']
	# school = findSchool(schData,'Broadhurst School')
	print "loading building data..."
	gmldoc,buildings = loadBuildings('data/TQ28.gml') # TODO
	print "calculating positions of buildings..."
	buildingsPos = loadBuildingsPos(buildings)

	schoolBuildings = []
	for school in schools:
		print school['name']
		building = findSchoolBuilding(buildings,buildingsPos,school['markpos'],'lat_long')
		schoolBuildings.append(building)
		annotateBuilding(gmldoc,building,school['markpos'],school['name'])
		savings,cost,years = calculatePV(building)
		print savings,cost,years
		write2csv((school['name'],savings,cost,years),'data/camden.csv')
		print ""

	print "writing new gml file..."
	createNewGml('data/camden_schools.gml',schoolBuildings)