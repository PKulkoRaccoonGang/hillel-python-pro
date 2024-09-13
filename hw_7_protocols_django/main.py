class Colorizer:
    """
    A context manager that changes the terminal text color to a specified color
    while the context is active and resets the color back to default afterward.

    Attributes:
        COLOR_PALLETE (dict): A dictionary mapping color names to ANSI escape codes
                              for terminal text colors.
        color (str): The ANSI escape code for the selected color.

    Methods:
        __init__(color):
            Initializes the Colorizer with the specified color. If the color is not found,
            it defaults to 'reset' (the default terminal color).

        __enter__():
            Called upon entering the context. Changes the terminal text color to the selected color.

        __exit__(exc_type, exc_value, traceback):
            Called upon exiting the context. Resets the terminal text color to default.
    """

    COLOR_PALLETE = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'default': '\033[99m'
    }

    def __init__(self, color):
        self.color = self.COLOR_PALLETE.get(color, self.COLOR_PALLETE['reset'])

    def __enter__(self):
        print(self.color, end='')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(self.COLOR_PALLETE['reset'], end='')


# yellow
print('\033[93m', end='')
print('aaa')
print('bbb')

# default
print('\033[0m', end='')
print('ccc')

with Colorizer('red'):
    print('printed in red')

print('printed in default color')

with Colorizer('green'):
    print('printed in green')

print('printed in default color')
