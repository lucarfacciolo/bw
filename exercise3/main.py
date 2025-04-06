from math import sqrt
from computed_property import computed_property


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property("x", "y", "z")
    def magnitude(self):
        print("computing magnitude")
        return sqrt(self.x**2 + self.y**2 + self.z**2)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property("radius")
    def diameter(self):  # type:ignore
        """Circle diameter from radius"""
        print("computing diameter")
        return self.radius * 2

    # NOTE(lfacciolo) by using the decorator, my function inherits properties from computed property
    @diameter.setter
    def diameter(self, value):  # type:ignore
        self.radius = value / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0


if __name__ == "__main__":
    v = Vector(9, 2, 6)
    v.magnitude
    v.color = "red"
    v.magnitude
    v.y = 18
    v.magnitude

    c = Circle()
    print(c.diameter)
    c.diameter = 3
    print(c.radius)
    del c.diameter
    print(c.radius)
