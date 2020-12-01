import unittest

from MeritFunctions import MeritFunctions


class TestMeritFunctionsTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class MeritFunctions """
        
        self.MeritFunctionsObj = MeritFunctions()

        self.BER = self.MeritFunctionsObj.BER
        self.SNR = self.MeritFunctionsObj.SNR
        self.DataRate = self.MeritFunctionsObj.DataRate
        
        pass


    def test_types(self):
        """ Function to test data types for class MeritFunctions """
        
        self.assertIsInstance(self.BER, list)
        self.assertIsInstance(self.SNR, float)
        self.assertIsInstance(self.DataRate, float)
        
        pass

class TestCalculateBER(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method MeritFunctions.calculateBER() """
        
        
        pass

class TestCalculateSNR(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method MeritFunctions.calculateSNR() """
        
        
        pass

class TestCalculateDataRate(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method MeritFunctions.calculateDataRate() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()