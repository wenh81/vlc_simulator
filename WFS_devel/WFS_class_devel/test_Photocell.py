import unittest

from Photocell import Photocell


class TestPhotocellTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Photocell """
        
        self.PhotocellObj = Photocell(PCq, PC_inner, PCc, area_Ph, G, PCs, QE, QE_inner, radius_inner, coefabs, reflect, Pcref, Dn, Dp, Ln, Lp, Wb, We, Sb)

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
        
        self.assertIsInstance(self.PCq, float)
        self.assertIsInstance(self.PC_inner, float)
        self.assertIsInstance(self.PCc, float)
        self.assertIsInstance(self.area_Ph, float)
        self.assertIsInstance(self.G, float)
        self.assertIsInstance(self.PCs, float)
        self.assertIsInstance(self.QE, float)
        self.assertIsInstance(self.QE_inner, float)
        self.assertIsInstance(self.radius_inner, float)
        self.assertIsInstance(self.coefabs, float)
        self.assertIsInstance(self.reflect, float)
        self.assertIsInstance(self.Pcref, float)
        self.assertIsInstance(self.Dn, float)
        self.assertIsInstance(self.Dp, float)
        self.assertIsInstance(self.Ln, float)
        self.assertIsInstance(self.Lp, float)
        self.assertIsInstance(self.Wb, float)
        self.assertIsInstance(self.We, float)
        self.assertIsInstance(self.Sb, float)
        
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