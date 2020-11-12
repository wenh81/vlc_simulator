import unittest

from LightSource import LightSource


class TestLightSourceTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class LightSource """
        
        self.LightSourceObj = LightSource(light_type, var1, var2)

        self.light_type = self.LightSourceObj.light_type
        self.psd = self.LightSourceObj.psd
        self.intensity = self.LightSourceObj.intensity
        self.database = self.LightSourceObj.database
        
        pass


    def test_types(self):
        """ Function to test data types for class LightSource """
        
        self.assertIsInstance(self.light_type, str)
        self.assertIsInstance(self.psd, dict)
        self.assertIsInstance(self.intensity, dict)
        self.assertIsInstance(self.database, str)
        
        pass

class TestGetIntensityAtDistance(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method LightSource.getIntensityAtDistance() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()