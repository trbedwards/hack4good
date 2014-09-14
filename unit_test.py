from gml_parser import *
from PVcalc import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.gmldoc = read_gml('data/barnet8.gml')
        self.buildings = extractElements(self.gmldoc)

    def test_calcArea(self):
        coordinates = extractCoordinates(self.buildings[0])
        self.assertTrue(calcArea(coordinates)>0)

    def setUpPVcalc(self):
    	buildingArea = calcBuildingArea(self.building)
    	self.area = calcAreaSolarPanels(buildingArea)
    	self.irr = solarIrradiance()
    	self.eta = efficiency()
    	self.Eg = calcEnergyGenerated(self.irr, self.area, self.eta)

    def calcMoneySaved(self):
    	self.P = powerInstalled(self.area)
    	self.M = moneySaved(self.Eg,self.P)
    	print "area = %f" % self.area
    	print "irradiance = %f" % self.irr
    	print "efficiency = %f" % self.eta
    	print "Power rating = %f kW" % self.P
    	print "Money saved = %f" % self.M
    	self.assertTrue(self.M>0)

    def calcCost(self):
    	self.cost = calcCostSolarPanels(self.P)

    def calcTimeForBreakEven(self):
		self.t = self.cost/self.M

    def test_loopOverBuildings(self):
    	for self.building in self.buildings:
	    	print extractValue(self.building,'vmd:School')
    		self.setUpPVcalc()	
    		self.calcMoneySaved()
    		self.calcCost()
    		print "Up front cost = %f" % self.cost
    		self.calcTimeForBreakEven()
    		print "time for breakeven = %f years" % self.t
    		print ""

if __name__ == '__main__':
    unittest.main()