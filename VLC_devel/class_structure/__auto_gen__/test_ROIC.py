import unittest

from ROIC import ROIC


class TestROICTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class ROIC """
        
        self.ROICObj = ROIC(circuit_type, circuit_simulation, which_simulator)

        self.circuit_type = self.ROICObj.circuit_type
        self.circuit_simulation = self.ROICObj.circuit_simulation
        self.linearity_curve = self.ROICObj.linearity_curve
        self.which_simulator = self.ROICObj.which_simulator
        self.netlist = self.ROICObj.netlist
        self.netlist_path = self.ROICObj.netlist_path
        
        pass


    def test_types(self):
        """ Function to test data types for class ROIC """
        
        self.assertIsInstance(self.circuit_type, str)
        self.assertIsInstance(self.circuit_simulation, bool)
        self.assertIsInstance(self.linearity_curve, dict)
        self.assertIsInstance(self.which_simulator, str)
        self.assertIsInstance(self.netlist, str)
        self.assertIsInstance(self.netlist_path, str)
        
        pass

class TestConvertsToVoltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method ROIC.convertsToVoltage() """
        
        
        pass

class TestCallSimulator(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method ROIC.callSimulator() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()