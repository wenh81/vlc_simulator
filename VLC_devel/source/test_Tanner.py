import unittest

from Tanner import Tanner


class TestTannerTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Tanner """
        
        self.TannerObj = Tanner(netlist, wave_names)

        self.netlist = self.TannerObj.netlist
        self.waves = self.TannerObj.waves
        
        pass


    def test_types(self):
        """ Function to test data types for class Tanner """
        
        self.assertIsInstance(self.netlist, str)
        self.assertIsInstance(self.waves, dict)
        
        pass

class TestSetupTanner(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Tanner.setupTanner() """
        
        
        pass

class TestStartTanner(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Tanner.startTanner() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()