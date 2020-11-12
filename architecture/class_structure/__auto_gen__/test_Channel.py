import unittest

from Channel import Channel


class TestChannelTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Channel """
        
        self.ChannelObj = Channel(ray_paths, ray_delays)

        self.ray_paths = self.ChannelObj.ray_paths
        self.ray_delays = self.ChannelObj.ray_delays
        
        pass


    def test_types(self):
        """ Function to test data types for class Channel """
        
        self.assertIsInstance(self.ray_paths, list)
        self.assertIsInstance(self.ray_delays, list)
        
        pass


if __name__ == '__main__':
    unittest.main()