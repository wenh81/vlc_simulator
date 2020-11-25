import unittest

from ADC import ADC


class TestADCTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class ADC """
        
        self.ADCObj = ADC(rx_data, circuit_simulation, bypass)

        self.rx_data_in = self.ADCObj.rx_data_in
        self.circuit_simulation = self.ADCObj.circuit_simulation
        self.bypass = self.ADCObj.bypass
        
        pass


    def test_types(self):
        """ Function to test data types for class ADC """
        
        self.assertIsInstance(self.rx_data_in, numpy.ndarray)
        self.assertIsInstance(self.circuit_simulation, bool)
        self.assertIsInstance(self.bypass, bool)
        
        pass

class TestConvertsToDigital(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method ADC.convertsToDigital() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()