import math


class Point:
    """
    A class representing a point in a 2D space.

    Attributes:
        x (float): The X coordinate of the point.
        y (float): The Y coordinate of the point.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point: ({self.x}, {self.y})'


class Circle:
    """
    A class representing a circle in a 2D space.

    Attributes:
        x (float): The X coordinate of the circle's center.
        y (float): The Y coordinate of the circle's center.
        radius (float): The radius of the circle.
    """
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        distance = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return distance <= self.radius

    def __str__(self):
        return f'Circle: ({self.x}, {self.y}, {self.radius})'


circle = Circle(0, 0, 5)
point_inside = Point(3, 4)
point_outside = Point(6, 8)

print(circle.contains(point_inside))
print(circle.contains(point_outside))
