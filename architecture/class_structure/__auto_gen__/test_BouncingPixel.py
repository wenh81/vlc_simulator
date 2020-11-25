import unittest

from BouncingPixel import BouncingPixel


class TestBouncingPixelTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class BouncingPixel """
        
        self.BouncingPixelObj = BouncingPixel(circuit_type, circuit_simulation, which_simulator)

        self.circuit_type = self.BouncingPixelObj.circuit_type
        self.circuit_simulation = self.BouncingPixelObj.circuit_simulation
        self.linearity_curve = self.BouncingPixelObj.linearity_curve
        self.which_simulator = self.BouncingPixelObj.which_simulator
        self.netlist = self.BouncingPixelObj.netlist
        self.netlist_path = self.BouncingPixelObj.netlist_path
        
        pass


    def test_types(self):
        """ Function to test data types for class BouncingPixel """
        
        self.assertIsInstance(self.circuit_type, str)
        self.assertIsInstance(self.circuit_simulation, bool)
        self.assertIsInstance(self.linearity_curve, dict)
        self.assertIsInstance(self.which_simulator, str)
        self.assertIsInstance(self.netlist, str)
        self.assertIsInstance(self.netlist_path, str)
        
        pass

class TestCalculatesReconstructedVoltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method BouncingPixel.calculatesReconstructedVoltage() """
        
        
        pass

class TestEditNetlist(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method BouncingPixel.editNetlist() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()