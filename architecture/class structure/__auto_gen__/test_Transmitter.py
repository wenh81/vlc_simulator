import unittest

from Transmitter import Transmitter


class TestTransmitterTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Transmitter """
        
        self.TransmitterObj = Transmitter(parent_var1, parent_var2)

        self.light_type = self.TransmitterObj.light_type
        
        pass


    def test_types(self):
        """ Function to test data types for class Transmitter """
        
        self.assertIsInstance(self.light_type, str)
        
        pass


if __name__ == '__main__':
    unittest.main()