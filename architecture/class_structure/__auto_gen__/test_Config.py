import unittest

from Config import Config


class TestConfigTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Config """
        
        self.ConfigObj = Config(n_transmitters, n_receivers)

        self.n_transmitters = self.ConfigObj.n_transmitters
        self.n_receivers = self.ConfigObj.n_receivers
        
        pass


    def test_types(self):
        """ Function to test data types for class Config """
        
        self.assertIsInstance(self.n_transmitters, int)
        self.assertIsInstance(self.n_receivers, int)
        
        pass


if __name__ == '__main__':
    unittest.main()