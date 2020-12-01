import unittest

from Message import Message


class TestMessageTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Message """
        
        self.MessageObj = Message(input_info, n_frames)

        self.input_info = self.MessageObj.input_info
        self.bitstream_frames = self.MessageObj.bitstream_frames
        self.number_of_frames = self.MessageObj.number_of_frames
        self.rx_bitstream_frames = self.MessageObj.rx_bitstream_frames
        self.output_info = self.MessageObj.output_info
        
        pass


    def test_types(self):
        """ Function to test data types for class Message """
        
        self.assertIsInstance(self.input_info, dict)
        self.assertIsInstance(self.bitstream_frames, list)
        self.assertIsInstance(self.number_of_frames, int)
        self.assertIsInstance(self.rx_bitstream_frames, list)
        self.assertIsInstance(self.output_info, dict)
        
        pass

class TestConvertsToBitstream(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Message.convertsToBitstream() """
        
        
        pass

class TestBitstreamToMessage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Message.BitstreamToMessage() """
        
        
        pass

class TestCompareMessages(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Message.compareMessages() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()