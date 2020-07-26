import unittest

from Circuit import Circuit


class TestCircuitTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Circuit """
        
        self.CircuitObj = Circuit(netlist, simulator)

        self.netlist = self.CircuitObj.netlist
        self.which_simulator = self.CircuitObj.which_simulator
        
        pass


    def test_types(self):
        """ Function to test data types for class Circuit """
        
        self.assertIsInstance(self.netlist, string)
        self.assertIsInstance(self.which_simulator, string)
        
        pass

class TestCalc_out_voltage(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Circuit.calc_out_voltage() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()