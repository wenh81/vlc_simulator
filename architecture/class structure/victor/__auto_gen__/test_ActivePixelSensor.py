import unittest

from ActivePixelSensor import ActivePixelSensor


class TestActivePixelSensorTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class ActivePixelSensor """
        
        self.ActivePixelSensorObj = ActivePixelSensor(netlist, simulator)

        self.netlist = self.ActivePixelSensorObj.netlist
        self.which_simulator = self.ActivePixelSensorObj.which_simulator
        
        pass


    def test_types(self):
        """ Function to test data types for class ActivePixelSensor """
        
        self.assertIsInstance(self.netlist, string)
        self.assertIsInstance(self.which_simulator, string)
        
        pass

class TestCalc_out_voltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method ActivePixelSensor.calc_out_voltage() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()