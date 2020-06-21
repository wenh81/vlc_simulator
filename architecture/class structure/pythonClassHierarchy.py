class Animal(object):
    def __init__(self):
        self.legs = 2
        self.name = 'Dog'
        self.color= 'Spotted'
        self.smell= 'Alot'
        self.age  = 10
        self.kids = 0
        #many more...


animal=Animal()

print(animal)
print()

attrs = vars(animal)
print(attrs)
print()

print(', '.join("%s: %s" % item for item in attrs.items()))

print()



print(dir(animal))
print()
