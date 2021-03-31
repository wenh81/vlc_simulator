import unittest

from Detector import Detector


class TestDetectorTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Detector """
        
        self.DetectorObj = Detector(light_type, position, angle)

        self.detector_type = self.DetectorObj.detector_type
        self.psd = self.DetectorObj.psd
        self.intensity = self.DetectorObj.intensity
        self.database = self.DetectorObj.database
        self.position = self.DetectorObj.position
        self.angle = self.DetectorObj.angle
        self.linearity_curve = self.DetectorObj.linearity_curve
        self.FOV = self.DetectorObj.FOV
        
        pass


    def test_types(self):
        """ Function to test data types for class Detector """
        
        self.assertIsInstance(self.detector_type, str)
        self.assertIsInstance(self.psd, dict)
        self.assertIsInstance(self.intensity, dict)
        self.assertIsInstance(self.database, str)
        self.assertIsInstance(self.position, list)
        self.assertIsInstance(self.angle, list)
        self.assertIsInstance(self.linearity_curve, dict)
        self.assertIsInstance(self.FOV, float)
        
        pass

class TestConvertsToPhotocurrent(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Detector.convertsToPhotocurrent() """
        
        
        pass

class TestLoadsJSONData(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Detector.loadsJSONData() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()