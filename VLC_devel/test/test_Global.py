import unittest

from Global import Global


class TestGlobalTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Global """
        
        self.GlobalObj = Global()

        self.transmitter_config = self.GlobalObj.transmitter_config
        self.receiver_config = self.GlobalObj.receiver_config
        self.wavelenghts = self.GlobalObj.wavelenghts
        self.temperature = self.GlobalObj.temperature
        self.which_simulator = self.GlobalObj.which_simulator
        
        pass


    def test_types(self):
        """ Function to test data types for class Global """
        
        self.assertIsInstance(self.transmitter_config, list)
        self.assertIsInstance(self.receiver_config, list)
        self.assertIsInstance(self.wavelenghts, list)
        self.assertIsInstance(self.temperature, float)
        self.assertIsInstance(self.which_simulator, str)
        
        pass


if __name__ == '__main__':
    unittest.main()