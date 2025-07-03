#!/usr/bin/env python3

import pyfiglet
import os

def print_full_width_line(character='-'):
    """
    Prints a line of the specified character that spans the entire terminal width.
    """
    try:
        terminal_width = os.get_terminal_size().columns
        line = character * terminal_width
        print(line)
    except OSError:
        # Handle cases where terminal size cannot be determined (e.g., not a TTY)
        print("Unable to determine terminal width. Printing a default long line.")
        print(character * 80)


user="Edward"
# Welcome Code
def greet():
    try:
        terminal_width = os.get_terminal_size().columns
        result = pyfiglet.figlet_format(f'Welcome, {user}', font="ANSI Shadow", width=terminal_width, justify="center")
    except OSError:
        result = pyfiglet.figlet_format(f'Welcome, {user}', font="ANSI Shadow", justify="center")
    print_full_width_line()
    print(result)
