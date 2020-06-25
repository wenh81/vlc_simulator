import unittest

from Quadcells import Quadcells


class TestQuadcellsTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Quadcells """
        
        self.QuadcellsObj = Quadcells(x, y, qc_type, has_microlens)

        self.x_pos = self.QuadcellsObj.x_pos
        self.y_pos = self.QuadcellsObj.y_pos
        self.qc_type = self.QuadcellsObj.qc_type
        self.has_microlens = self.QuadcellsObj.has_microlens
        
        pass


    def test_types(self):
        """ Function to test data types for class Quadcells """
        
        self.assertIsInstance(self.x_pos, int)
        self.assertIsInstance(self.y_pos, int)
        self.assertIsInstance(self.qc_type, str)
        self.assertIsInstance(self.has_microlens, bool)
        
        pass


if __name__ == '__main__':
    unittest.main()