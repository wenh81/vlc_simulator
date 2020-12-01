import unittest

from Main import Main


class TestMainTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Main """
        
        self.MainObj = Main()

        self.message_obj = self.MainObj.message_obj
        self.mapping_obj = self.MainObj.mapping_obj
        self.modulator_obj = self.MainObj.modulator_obj
        self.transmitter_obj = self.MainObj.transmitter_obj
        self.channel_obj = self.MainObj.channel_obj
        self.receiver_obj = self.MainObj.receiver_obj
        self.merit_functions_obj = self.MainObj.merit_functions_obj
        self.global_obj = self.MainObj.global_obj
        
        pass


    def test_types(self):
        """ Function to test data types for class Main """
        
        self.assertIsInstance(self.message_obj, Message)
        self.assertIsInstance(self.mapping_obj, Mapping)
        self.assertIsInstance(self.modulator_obj, Modulator)
        self.assertIsInstance(self.transmitter_obj, Transmitter)
        self.assertIsInstance(self.channel_obj, Channel)
        self.assertIsInstance(self.receiver_obj, Receiver)
        self.assertIsInstance(self.merit_functions_obj, MeritFunctions)
        self.assertIsInstance(self.global_obj, Global)
        
        pass


if __name__ == '__main__':
    unittest.main()