from gml_parser import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.gmldoc = read_gml('data/barnet8.gml')
        self.buildings = extractElements(self.gmldoc)

    def test_calcArea(self):
        coordinates = extractCoordinates(self.buildings[0])
        self.assertTrue(calcArea(coordinates)>0)

if __name__ == '__main__':
    unittest.main()