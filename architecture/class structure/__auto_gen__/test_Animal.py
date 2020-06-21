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


    def testTypes(self):
        """ Function to test data types for class Animal """
        
        self.assertIsInstance(self.var1, float)
        self.assertIsInstance(self.var2, str)
        self.assertIsInstance(self.var3, int)
        
        pass

class TestFunc1(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Animal.func1() """
        
        self.AnimalObj = Animal()

        self.var1 = self.AnimalObj.var1
        self.var2 = self.AnimalObj.var2
        self.var3 = self.AnimalObj.var3
        
        pass


    def testTypes(self):
        """ Function to test data types for method Animal.func1() """
        
        self.assertIsInstance(self.var1, float)
        self.assertIsInstance(self.var2, str)
        self.assertIsInstance(self.var3, int)
        
        pass

class TestFunc2(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Animal.func2() """
        
        self.AnimalObj = Animal()

        self.var1 = self.AnimalObj.var1
        self.var2 = self.AnimalObj.var2
        self.var3 = self.AnimalObj.var3
        
        pass


    def testTypes(self):
        """ Function to test data types for method Animal.func2() """
        
        self.assertIsInstance(self.var1, float)
        self.assertIsInstance(self.var2, str)
        self.assertIsInstance(self.var3, int)
        
        pass


if __name__ == '__main__':
    unittest.main()