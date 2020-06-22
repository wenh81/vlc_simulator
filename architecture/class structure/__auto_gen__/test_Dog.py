import unittest

from Dog import Dog


class TestDogTypes(unittest.TestCase):
    
    def setUp(self):
        """ Setup function TestTypes for class Dog """
        
        self.DogObj = Dog(barkSound, dogAge, dogName)

        self.name = self.DogObj.name
        self.age = self.DogObj.age
        self.type = self.DogObj.type
        self.barkSound = self.DogObj.barkSound
        
        pass


    def test_types(self):
        """ Function to test data types for class Dog """
        
        self.assertIsInstance(self.name, str)
        self.assertIsInstance(self.age, int)
        self.assertIsInstance(self.type, str)
        self.assertIsInstance(self.barkSound, str)
        
        pass


if __name__ == '__main__':
    unittest.main()