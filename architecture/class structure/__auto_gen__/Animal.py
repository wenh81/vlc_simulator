class Animal(object):
    def __init__(self, age, banana):
        """Constructor"""

        # Stores name
        self.name = banana
        self.age = age
    
        pass

    def speak(self):
        """The animal speaks. Has no arguments."""
        pass


    def anotherMethod(self):
        """The animal speaks. Has no arguments."""
        
        self.speak()
    
