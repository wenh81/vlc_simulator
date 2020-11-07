import unittest

from Photocell import Photocell


class TestPhotocellTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Photocell """
        
        self.PhotocellObj = Photocell()

        self.PCq = self.PhotocellObj.PCq
        self.PC_inner = self.PhotocellObj.PC_inner
        self.PCc = self.PhotocellObj.PCc
        self.area_Ph = self.PhotocellObj.area_Ph
        self.G = self.PhotocellObj.G
        self.PCs = self.PhotocellObj.PCs
        self.QE = self.PhotocellObj.QE
        self.QE_inner = self.PhotocellObj.QE_inner
        self.radius_inner = self.PhotocellObj.radius_inner
        self.coefabs = self.PhotocellObj.coefabs
        self.reflect = self.PhotocellObj.reflect
        self.Pcref = self.PhotocellObj.Pcref
        self.Dn = self.PhotocellObj.Dn
        self.Dp = self.PhotocellObj.Dp
        self.Ln = self.PhotocellObj.Ln
        self.Lp = self.PhotocellObj.Lp
        self.Wb = self.PhotocellObj.Wb
        self.We = self.PhotocellObj.We
        self.Sb = self.PhotocellObj.Sb
        
        pass


    def test_types(self):
        """ Function to test data types for class Photocell """
        
        self.assertIsInstance(self.PCq, double)
        self.assertIsInstance(self.PC_inner, double)
        self.assertIsInstance(self.PCc, double)
        self.assertIsInstance(self.area_Ph, double)
        self.assertIsInstance(self.G, double)
        self.assertIsInstance(self.PCs, double)
        self.assertIsInstance(self.QE, double)
        self.assertIsInstance(self.QE_inner, double)
        self.assertIsInstance(self.radius_inner, double)
        self.assertIsInstance(self.coefabs, double)
        self.assertIsInstance(self.reflect, double)
        self.assertIsInstance(self.Pcref, double)
        self.assertIsInstance(self.Dn, double)
        self.assertIsInstance(self.Dp, double)
        self.assertIsInstance(self.Ln, double)
        self.assertIsInstance(self.Lp, double)
        self.assertIsInstance(self.Wb, double)
        self.assertIsInstance(self.We, double)
        self.assertIsInstance(self.Sb, double)
        
        pass

class TestCalcPhotoCurrent()(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Photocell.calcPhotoCurrent()() """
        
        
        pass

class TestGetPhotoCurrent()(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Photocell.getPhotoCurrent()() """
        
        
        pass

class TestInitiAllConfig(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Photocell.initiAllConfig() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()