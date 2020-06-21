import unittest

from Transmitter import Transmitter


class TestTransmitterTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Transmitter """
        
        self.TransmitterObj = Transmitter()

        self.light_type = self.TransmitterObj.light_type
        self.psd = self.TransmitterObj.psd
        self.intensity = self.TransmitterObj.intensity
        self.database = self.TransmitterObj.database
        
        pass


    def test_types(self):
        """ Function to test data types for class Transmitter """
        
        self.assertIsInstance(self.light_type, float)
        self.assertIsInstance(self.psd, str)
        self.assertIsInstance(self.intensity, int)
        self.assertIsInstance(self.database, json)
        
        pass

class TestFunc1(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.func1() """
        
        
        pass

class TestFunc2(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Transmitter.func2() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()