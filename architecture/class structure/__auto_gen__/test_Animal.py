import unittest

from Animal import Animal


class TestAnimalTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Animal """
        
        self.AnimalObj = Animal(age, name)

        self.name = self.AnimalObj.name
        self.age = self.AnimalObj.age
        
        pass


    def test_types(self):
        """ Function to test data types for class Animal """
        
        self.assertIsInstance(self.name, str)
        self.assertIsInstance(self.age, int)
        
        pass

class TestSpeak(unittest.TestCase):
    
    def setUp(self):
        """ Setup function to test method Animal.speak() """
        
        
        pass


if __name__ == '__main__':
    unittest.main()