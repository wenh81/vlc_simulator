import unittest

from Dog import Dog


class TestDogTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Dog """
        
        self.DogObj = Dog()

        self.var1 = self.DogObj.var1
        self.var2 = self.DogObj.var2
        self.var3 = self.DogObj.var3
        
        pass


    def test_types(self):
        """ Function to test data types for class Dog """
        
        self.assertIsInstance(self.var1, float)
        self.assertIsInstance(self.var2, str)
        self.assertIsInstance(self.var3, int)
        
        pass

class TestFunc1(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Dog.func1() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()