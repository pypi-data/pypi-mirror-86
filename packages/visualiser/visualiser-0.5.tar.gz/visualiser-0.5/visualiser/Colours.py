import sys

class Colours:
    def __init__(self):
        self.red   = "\033[1;31m"  
        self.blue  = "\033[1;34m"
        self.cyan  = "\033[1;36m"
        self.green = "\033[0;32m"
        self.reset = "\033[0;0m"
        self.bold    = "\033[;1m"

        self.spectrum = [
            self.red,
            self.red,
            self.green,
            self.green,
            self.green,
            self.green,
            self.cyan,
            self.cyan,
            self.cyan,
            self.cyan,
            self.blue,
            self.blue,
        ]

    def reset_colours(self):
        sys.stdout.write(self.reset)

    def set_colour(self, index):
        sys.stdout.write(self.spectrum[index])