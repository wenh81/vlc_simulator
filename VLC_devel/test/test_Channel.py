import unittest

from Channel import Channel


class TestChannelTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Channel """
        
        self.ChannelObj = Channel(tx_data_in, raytrace)

        self.tx_data_in = self.ChannelObj.tx_data_in
        self.raytrace = self.ChannelObj.raytrace
        self.channel_response = self.ChannelObj.channel_response
        self.rx_convolved = self.ChannelObj.rx_convolved
        self.rx_SNR = self.ChannelObj.rx_SNR
        self.rx_optical_power = self.ChannelObj.rx_optical_power
        self.rx_std = self.ChannelObj.rx_std
        self.rx_noise = self.ChannelObj.rx_noise
        self.rx_data_out = self.ChannelObj.rx_data_out
        
        pass


    def test_types(self):
        """ Function to test data types for class Channel """
        
        self.assertIsInstance(self.tx_data_in, numpy.ndarray)
        self.assertIsInstance(self.raytrace, bool)
        self.assertIsInstance(self.channel_response, list)
        self.assertIsInstance(self.rx_convolved, numpy.ndarray)
        self.assertIsInstance(self.rx_SNR, float)
        self.assertIsInstance(self.rx_optical_power, float)
        self.assertIsInstance(self.rx_std, float)
        self.assertIsInstance(self.rx_noise, numpy.ndarray)
        self.assertIsInstance(self.rx_data_out, numpy.ndarray)
        
        pass

class TestCalculatesChannelResponse(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Channel.calculatesChannelResponse() """
        
        
        pass

class TestApplyChannelResponse(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Channel.applyChannelResponse() """
        
        
        pass

class TestCalculatesReceiverSNR(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Channel.calculatesReceiverSNR() """
        
        
        pass

class TestApplyChannelNoise(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Channel.applyChannelNoise() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()