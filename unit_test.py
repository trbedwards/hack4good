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
    	buildingArea = calcBuildingArea(self.buildings[0])
    	self.area = calcAreaSolarPanels(buildingArea)
    	self.irr = solarIrradiance()
    	self.eta = efficiency()

    def test_calcEg(self):
    	self.setUpPVcalc()
    	self.assertTrue(self.energyGen()>0)

    def energyGen(self):
    	return calcEnergyGenerated(self.irr, self.area, self.eta)

    def test_calcMoneySaved(self):
    	self.setUpPVcalc()
    	print "area = %f" % self.area
    	print "irradiance = %f" % self.irr
    	print "efficiency = %f" % self.eta
    	P = powerInstalled(self.area)
    	M = moneySaved(self.energyGen(),P)
    	print "Power rating = %f kW" % P
    	print "Money saved = %f" % M
    	self.assertTrue(M>0)

if __name__ == '__main__':
    unittest.main()