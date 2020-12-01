import unittest

from Simulator import Simulator


class TestSimulatorTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Simulator """
        
        self.SimulatorObj = Simulator(netlist)

        self.simul_timeout = self.SimulatorObj.simul_timeout
        self.netlist = self.SimulatorObj.netlist
        
        pass


    def test_types(self):
        """ Function to test data types for class Simulator """
        
        self.assertIsInstance(self.simul_timeout, int)
        self.assertIsInstance(self.netlist, str)
        
        pass

class TestStopSimulation(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Simulator.stopSimulation() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()