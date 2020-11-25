import unittest

from Modulator import Modulator


class TestModulatorTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Modulator """
        
        self.ModulatorObj = Modulator(mapped_info, modulation_type)

        self.mapped_info = self.ModulatorObj.mapped_info
        self.mapped_shape = self.ModulatorObj.mapped_shape
        self.bits_per_symbol = self.ModulatorObj.bits_per_symbol
        self.frame_size = self.ModulatorObj.frame_size
        self.modulation_type = self.ModulatorObj.modulation_type
        
        pass


    def test_types(self):
        """ Function to test data types for class Modulator """
        
        self.assertIsInstance(self.mapped_info, numpy.ndarray)
        self.assertIsInstance(self.mapped_shape, tuple)
        self.assertIsInstance(self.bits_per_symbol, int)
        self.assertIsInstance(self.frame_size, int)
        self.assertIsInstance(self.modulation_type, str)
        
        pass

class TestCreateModulator(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Modulator.createModulator() """
        
        
        pass

class TestApplyModulation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Modulator.applyModulation() """
        
        
        pass

class TestApplyDemodulation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Modulator.applyDemodulation() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()