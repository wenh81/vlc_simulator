import unittest

from Transmitter import Transmitter


class TestTransmitterTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Transmitter """
        
        self.TransmitterObj = Transmitter(transmitter_config, tx_data, bypass)

        self.transmitter_config = self.TransmitterObj.transmitter_config
        self.tx_data_in = self.TransmitterObj.tx_data_in
        self.bypass = self.TransmitterObj.bypass
        
        pass


    def test_types(self):
        """ Function to test data types for class Transmitter """
        
        self.assertIsInstance(self.transmitter_config, list)
        self.assertIsInstance(self.tx_data_in, numpy.ndarray)
        self.assertIsInstance(self.bypass, bool)
        
        pass

class TestCreateAllLamps(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.createAllLamps() """
        
        
        pass

class TestCreateLamp(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.createLamp() """
        
        
        pass

class TestApplyDAC(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.applyDAC() """
        
        
        pass

class TestCalculatesOpticalPower(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.calculatesOpticalPower() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()