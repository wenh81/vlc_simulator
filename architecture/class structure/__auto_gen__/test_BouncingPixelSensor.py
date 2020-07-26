import unittest

from BouncingPixelSensor import BouncingPixelSensor


class TestBouncingPixelSensorTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class BouncingPixelSensor """
        
        self.BouncingPixelSensorObj = BouncingPixelSensor(netlist, simulator)

        self.netlist = self.BouncingPixelSensorObj.netlist
        self.which_simulator = self.BouncingPixelSensorObj.which_simulator
        
        pass


    def test_types(self):
        """ Function to test data types for class BouncingPixelSensor """
        
        self.assertIsInstance(self.netlist, string)
        self.assertIsInstance(self.which_simulator, string)
        
        pass

class TestCalc_out_voltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method BouncingPixelSensor.calc_out_voltage() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()