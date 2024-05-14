class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        print(f"hello,{self.name},{self.age}")

person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

person1.greet()
person2.greet()
