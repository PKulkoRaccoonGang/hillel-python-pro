class Frange:
    """
    A custom range generator that supports floating-point numbers and customizable step sizes.
    This class behaves similarly to Python's built-in range function but allows for more flexibility
    with start, end, and step values.

    Attributes:
        start_value (float or int): The starting value of the range.
        end_value (float or int): The ending value of the range (exclusive).
        step (float or int): The step by which the range increments or decrements.
        current_value (float or int): The current value during iteration.

    Methods:
        __init__(start_value, end_value=None, step=1):
            Initializes the Frange object with the provided start, end, and step values.

        __iter__():
            Resets the current_value and returns the iterator itself.

        __next__():
            Returns the next value in the range. Raises StopIteration when the end of the range is reached.
    """
    def __init__(self, start_value, end_value=None, step=1) -> None:
        if end_value is None:
            end_value = start_value
            start_value = 0
        self.start_value = start_value
        self.end_value = end_value
        self.step = step
        self.current_value = self.start_value

    def __iter__(self):
        """
        Resets the current value to the start value and returns the iterator.

        Returns:
            Frange: The iterator object itself.
        """
        self.current_value = self.start_value
        return self

    def __next__(self):
        """
        Returns the next value in the range. If the current value exceeds the end value
        (or is less than for negative steps), raises StopIteration to signal the end of iteration.

        Returns:
            float or int: The next value in the range.

        Raises:
            StopIteration: If the current value exceeds or falls below the end value, depending on the step direction.
        """
        if (self.step > 0 and self.current_value >= self.end_value) or (self.step < 0 and self.current_value <= self.end_value):
            raise StopIteration
        result = self.current_value
        self.current_value += self.step
        return result


assert (list(Frange(5)) == [0, 1, 2, 3, 4])
assert (list(Frange(2, 5)) == [2, 3, 4])
assert (list(Frange(2, 10, 2)) == [2, 4, 6, 8])
assert (list(Frange(10, 2, -2)) == [10, 8, 6, 4])
assert (list(Frange(2, 5.5, 1.5)) == [2, 3.5, 5])
assert (list(Frange(1, 5)) == [1, 2, 3, 4])
assert (list(Frange(0, 5)) == [0, 1, 2, 3, 4])
assert (list(Frange(0, 0)) == [])
assert (list(Frange(100, 0)) == [])

print('SUCCESS!')
