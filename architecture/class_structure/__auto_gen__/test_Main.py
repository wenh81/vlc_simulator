import unittest

from Main import Main


class TestMainTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Main """
        
        self.MainObj = Main(transmitter_array, channel_obj, receiver_array, simulator_obj, global_obj)

        self.transmitter_array = self.MainObj.transmitter_array
        self.channel_obj = self.MainObj.channel_obj
        self.receiver_array = self.MainObj.receiver_array
        self.simulator_obj = self.MainObj.simulator_obj
        self.global_obj = self.MainObj.global_obj
        
        pass


    def test_types(self):
        """ Function to test data types for class Main """
        
        self.assertIsInstance(self.transmitter_array, list)
        self.assertIsInstance(self.channel_obj, Channel)
        self.assertIsInstance(self.receiver_array, Receiver)
        self.assertIsInstance(self.simulator_obj, Simulator)
        self.assertIsInstance(self.global_obj, Global)
        
        pass


if __name__ == '__main__':
    unittest.main()