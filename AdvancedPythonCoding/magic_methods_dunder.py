class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def __del__(self):
        print("Object is being deconstructed!")


# p = Person("Michael", 26)

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}"
    
    def __len__(self):
        return (x**2 + y**2)**0.5 # length of vector

    def __call__(self):
        print("Hey, you called me?")
    
    


v1 = Vector(10, 20)
v2 = Vector(50, 60)
v3 = v1 + v2
print(v3)
v3()

