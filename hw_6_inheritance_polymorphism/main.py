import math


class Shape:
    """Base class for shapes with coordinates (x, y)."""

    def __init__(self, x, y):
        """
        Initialize the Shape with coordinates.

        :param x: X-coordinate of the shape
        :param y: Y-coordinate of the shape
        """
        self.x = x
        self.y = y

    def square(self):
        """
        Return the area of the shape. To be overridden by subclasses.
        :return: Area of the shape (default is 0)
        """
        return 0


class Point(Shape):
    """A class representing a point in the 2D space."""
    pass


class Circle(Shape):
    """A class representing a circle."""

    def __init__(self, x, y, radius):
        """
        Initialize a circle with center coordinates and a radius.

        :param x: X-coordinate of the center
        :param y: Y-coordinate of the center
        :param radius: Radius of the circle
        :raise ValueError: If radius is non-positive
        """
        super().__init__(x, y)
        if radius <= 0:
            raise ValueError('Radius must be a positive number.')
        self.radius = radius

    def square(self):
        """
        Calculate and return the area of the circle.
        :return: Area of the circle
        """
        return math.pi * self.radius ** 2

    def __contains__(self, other):
        """
        Check if a point lies within the circle.
        :param other: Point object to check
        :return: True if point lies inside the circle, False otherwise
        :raise ValueError: If other is not a Point
        """
        if not isinstance(other, Point):
            raise ValueError('This operation is available only for Point')
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2 <= self.radius ** 2

    def __repr__(self):
        return f'Circle(x={self.x}, y={self.y}, radius={self.radius})'


class Rectangle(Shape):
    """A class representing a rectangle."""

    def __init__(self, x, y, height, width):
        """
        Initialize a rectangle with top-left corner coordinates, height, and width.

        :param x: X-coordinate of the top-left corner
        :param y: Y-coordinate of the top-left corner
        :param height: Height of the rectangle
        :param width: Width of the rectangle
        :raise ValueError: If height or width is non-positive
        """
        super().__init__(x, y)
        if height <= 0 or width <= 0:
            raise ValueError('Height and width must be positive numbers.')
        self.height = height
        self.width = width

    def square(self):
        """
        Calculate and return the area of the rectangle.
        :return: Area of the rectangle
        """
        return self.width * self.height

    def __repr__(self):
        return f'Rectangle(x={self.x}, y={self.y}, height={self.height}, width={self.width})'


class Parallelogram(Rectangle):
    """A class representing a parallelogram."""

    def __init__(self, x, y, height, width, angle):
        """
        Initialize a parallelogram with base coordinates, height, width, and angle between sides.

        :param x: X-coordinate of the base
        :param y: Y-coordinate of the base
        :param height: Height of the parallelogram
        :param width: Width of the parallelogram
        :param angle: Angle between sides (in degrees)
        :raise ValueError: If the angle is not between 0 and 180 degrees
        """
        super().__init__(x, y, height, width)
        if angle <= 0 or angle >= 180:
            raise ValueError('Angle must be between 0 and 180 degrees (non-inclusive).')
        self.angle = angle

    def square(self):
        """
        Calculate and return the area of the parallelogram.
        :return: Area of the parallelogram
        """
        return self.height * math.sin(math.radians(self.angle)) * self.width

    def __str__(self):
        return f'Parallelogram: width={self.width}, height={self.height}, angle={self.angle}'


class Triangle(Shape):
    """A class representing a triangle."""

    def __init__(self, x, y, a, b, c):
        """
        Initialize a triangle with three sides.

        :param x: X-coordinate of the base
        :param y: Y-coordinate of the base
        :param a: Length of side a
        :param b: Length of side b
        :param c: Length of side c
        :raise ValueError: If sides are non-positive or don't form a valid triangle
        """
        super().__init__(x, y)
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError('Sides must be positive.')
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError(
                'The sum of the lengths of any two sides must be greater than the length of the third side.')
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        """
        Calculate and return the perimeter of the triangle.
        :return: Perimeter of the triangle
        """
        return self.a + self.b + self.c

    @property
    def semi_perimeter(self):
        """
        Calculate and return the semi-perimeter of the triangle.
        :return: Semi-perimeter of the triangle
        """
        return self.perimeter() / 2

    def square(self):
        """
        Calculate and return the area of the triangle using Heron's formula.
        :return: Area of the triangle
        """
        return math.sqrt(
            self.semi_perimeter *
            (self.semi_perimeter - self.a) *
            (self.semi_perimeter - self.b) *
            (self.semi_perimeter - self.c)
        )

    def __repr__(self):
        return f'Triangle(x={self.x}, y={self.y}, a={self.a}, b={self.b}, c={self.c})'


class Scene:
    """A class representing a collection of shapes."""

    def __init__(self):
        """Initialize an empty scene."""
        self._figures = []

    def add_figure(self, figure):
        """
        Add a figure to the scene.

        :param figure: A shape to add to the scene
        """
        self._figures.append(figure)

    def total_square(self):
        """
        Calculate and return the total area of all figures in the scene.
        :return: Total area of the figures
        """
        return sum(f.square() for f in self._figures)

    def __str__(self):
        """
        Return a string representation of all the figures in the scene.
        :return: String listing all figures in the scene
        """
        return "\n".join([str(f) for f in self._figures])


scene = Scene()
scene.add_figure(Rectangle(0, 0, 10, 20))
scene.add_figure(Circle(10, 0, 10))
scene.add_figure(Parallelogram(1, 2, 18, 23, 38))
scene.add_figure(Triangle(20, 5, 10, 20, 27))

print(f"Scene's total square: {scene.total_square()}")
