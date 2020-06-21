import unittest

from Animal import Animal


class TestAnimalTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Animal """
        
        self.AnimalObj = Animal()

        self.var1 = self.AnimalObj.var1
        self.var2 = self.AnimalObj.var2
        self.var3 = self.AnimalObj.var3
        
        pass


    def test_types(self):
        """ Function to test data types for class Animal """
        
        self.assertIsInstance(self.var1, float)
        self.assertIsInstance(self.var2, str)
        self.assertIsInstance(self.var3, int)
        
        pass

class TestFunc1(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Animal.func1() """
        
        
        pass

class TestFunc2(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Animal.func2() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()