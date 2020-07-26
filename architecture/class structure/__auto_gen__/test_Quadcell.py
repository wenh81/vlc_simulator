import unittest

from Quadcell import Quadcell


class TestQuadcellTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Quadcell """
        
        self.QuadcellObj = Quadcell(x, y, qc_type, has_microlens)

        self.nn = self.QuadcellObj.nn
        self.theta = self.QuadcellObj.theta
        self.jx = self.QuadcellObj.jx
        self.jy = self.QuadcellObj.jy
        self.na = self.QuadcellObj.na
        self.ma = self.QuadcellObj.ma
        self.xx = self.QuadcellObj.xx
        self.outx_l = self.QuadcellObj.outx_l
        self.outx = self.QuadcellObj.outx
        self.outy = self.QuadcellObj.outy
        self.cell_qc = self.QuadcellObj.cell_qc
        self.stepp = self.QuadcellObj.stepp
        self.slope = self.QuadcellObj.slope
        self.slope_ex = self.QuadcellObj.slope_ex
        self.x_edge = self.QuadcellObj.x_edge
        self.qc_type = self.QuadcellObj.qc_type
        self.has_microlens = self.QuadcellObj.has_microlens
        self.A_intensity = self.QuadcellObj.A_intensity
        self.B_intensity = self.QuadcellObj.B_intensity
        self.C_intensity = self.QuadcellObj.C_intensity
        self.D_intensity = self.QuadcellObj.D_intensity
        
        pass


    def test_types(self):
        """ Function to test data types for class Quadcell """
        
        self.assertIsInstance(self.nn, int)
        self.assertIsInstance(self.theta, str)
        self.assertIsInstance(self.jx, bool)
        self.assertIsInstance(self.jy, float)
        self.assertIsInstance(self.na, int)
        self.assertIsInstance(self.ma, int)
        self.assertIsInstance(self.xx, float)
        self.assertIsInstance(self.outx_l, float)
        self.assertIsInstance(self.outx, float)
        self.assertIsInstance(self.outy, float)
        self.assertIsInstance(self.cell_qc, float)
        self.assertIsInstance(self.stepp, int)
        self.assertIsInstance(self.slope, float)
        self.assertIsInstance(self.slope_ex, float)
        self.assertIsInstance(self.x_edge, float)
        self.assertIsInstance(self.qc_type, string)
        self.assertIsInstance(self.has_microlens, bool)
        self.assertIsInstance(self.A_intensity, float)
        self.assertIsInstance(self.B_intensity, float)
        self.assertIsInstance(self.C_intensity, float)
        self.assertIsInstance(self.D_intensity, float)
        
        pass

class TestCalcAllIntensities(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.calcAllIntensities() """
        
        
        pass

class TestGetIntensitiy(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.getIntensitiy() """
        
        
        pass

class TestGetPhotoCurrent(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.getPhotoCurrent() """
        
        
        pass

class TestCalcAllPhotoCurrents(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.calcAllPhotoCurrents() """
        
        
        pass

class TestCalcSpotCoordinates(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.calcSpotCoordinates() """
        
        
        pass

class TestGetOutX(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.getOutX() """
        
        
        pass

class TestGetOutY(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Quadcell.getOutY() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()