import unittest

from DAC import DAC


class TestDACTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class DAC """
        
        self.DACObj = DAC(tx_data, circuit_simulation, bypass)

        self.tx_data_in = self.DACObj.tx_data_in
        self.circuit_simulation = self.DACObj.circuit_simulation
        self.bypass = self.DACObj.bypass
        
        pass


    def test_types(self):
        """ Function to test data types for class DAC """
        
        self.assertIsInstance(self.tx_data_in, numpy.ndarray)
        self.assertIsInstance(self.circuit_simulation, bool)
        self.assertIsInstance(self.bypass, bool)
        
        pass

class TestConvertsToAnalog(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method DAC.convertsToAnalog() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()