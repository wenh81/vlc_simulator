import unittest

from Simulation import Simulation


class TestSimulationTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Simulation """
        
        self.SimulationObj = Simulation()

        
        pass


    def test_types(self):
        """ Function to test data types for class Simulation """
        
        
        pass

class TestAppend_list_to_file(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Simulation.append_list_to_file() """
        
        
        pass

class TestRead_from_file(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Simulation.read_from_file() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()