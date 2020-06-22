from Animal import Animal

class Dog(Animal):
    def __init__(self, barkSound, dogAge, dogName):
        """Constructor"""

        Animal.__init__(self, age = dogAge, name = dogName)
        

        # Stores name
        self.name = dogName
        self.age = dogAge

        # Type for that class.
        self.type = "dog"

        # Bark sound.
        self.barkSound = barkSound
    
        pass
