import os


def clear_screen():
    """Clears the console screen."""
    os.system("clear" if os.name == "posix" else "cls")
