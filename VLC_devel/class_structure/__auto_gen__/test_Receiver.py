import unittest

from Receiver import Receiver


class TestReceiverTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Receiver """
        
        self.ReceiverObj = Receiver(receiver_config, rx_data, bypass)

        self.receiver_config = self.ReceiverObj.receiver_config
        self.rx_data_in = self.ReceiverObj.rx_data_in
        self.bypass = self.ReceiverObj.bypass
        
        pass


    def test_types(self):
        """ Function to test data types for class Receiver """
        
        self.assertIsInstance(self.receiver_config, list)
        self.assertIsInstance(self.rx_data_in, numpy.ndarray)
        self.assertIsInstance(self.bypass, bool)
        
        pass

class TestCreateAllDetectors(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Receiver.createAllDetectors() """
        
        
        pass

class TestCreateDetector(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Receiver.createDetector() """
        
        
        pass

class TestCalculatesPhotocurrent(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Receiver.calculatesPhotocurrent() """
        
        
        pass

class TestCalculatesOutVoltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Receiver.calculatesOutVoltage() """
        
        
        pass

class TestApplyADC(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Receiver.applyADC() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()