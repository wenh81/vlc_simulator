import unittest

from LightSource import LightSource


class TestLightSourceTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class LightSource """
        
        self.LightSourceObj = LightSource(light_type, position, angle)

        self.light_type = self.LightSourceObj.light_type
        self.psd = self.LightSourceObj.psd
        self.intensity = self.LightSourceObj.intensity
        self.database = self.LightSourceObj.database
        self.position = self.LightSourceObj.position
        self.angle = self.LightSourceObj.angle
        self.linearity_curve = self.LightSourceObj.linearity_curve
        self.FOV = self.LightSourceObj.FOV
        
        pass


    def test_types(self):
        """ Function to test data types for class LightSource """
        
        self.assertIsInstance(self.light_type, str)
        self.assertIsInstance(self.psd, dict)
        self.assertIsInstance(self.intensity, dict)
        self.assertIsInstance(self.database, str)
        self.assertIsInstance(self.position, list)
        self.assertIsInstance(self.angle, list)
        self.assertIsInstance(self.linearity_curve, dict)
        self.assertIsInstance(self.FOV, float)
        
        pass

class TestConvertToOpticalPower(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method LightSource.convertToOpticalPower() """
        
        
        pass

class TestGetIntensityAtDistance(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method LightSource.getIntensityAtDistance() """
        
        
        pass

class TestLoadsJSONData(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method LightSource.loadsJSONData() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()