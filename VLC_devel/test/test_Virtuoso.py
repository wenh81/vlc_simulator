import unittest

from Virtuoso import Virtuoso


class TestVirtuosoTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Virtuoso """
        
        self.VirtuosoObj = Virtuoso(netlist, wave_names)

        self.netlist = self.VirtuosoObj.netlist
        self.waves = self.VirtuosoObj.waves
        
        pass


    def test_types(self):
        """ Function to test data types for class Virtuoso """
        
        self.assertIsInstance(self.netlist, str)
        self.assertIsInstance(self.waves, dict)
        
        pass

class TestSetupVirtuoso(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Virtuoso.setupVirtuoso() """
        
        
        pass

class TestStartVirtuoso(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Virtuoso.startVirtuoso() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()