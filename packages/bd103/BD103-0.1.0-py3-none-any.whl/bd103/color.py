'''
Color Module for the BD103 Package
'''

def print(text, color):
    if color == "reset":
        print("\u001b[0m" + text)
    elif color == "red":
        print("\u001b[31m" + text + "\u001b[0m")
    elif color == "yellow":
        print("\u001b[33m" + text + "\u001b[0m")
    elif color == "green":
        print("\u001b[32m" + text + "\u001b[0m")
    elif color == "cyan":
        print("\u001b[36m" + text + "\u001b[0m")
    elif color == "blue":
        print("\u001b[34m" + text + "\u001b[0m")
    elif color == "magenta":
        print("\u001b[35m" + text + "\u001b[0m")
    elif color == "black":
        print("\u001b[30m" + text + "\u001b[0m")
    elif color == "white":
        print("\u001b[37m" + text + "\u001b[0m")

def paint(color):
    if color == "reset":
        print("", "reset")
    elif color == "red":
        print("", "red")
    elif color == "yellow":
        print("", "yellow")
    elif color == "green":
        print("", "green")
    elif color == "cyan":
        print("", "cyan")
    elif color == "blue":
        print("", "blue")
    elif color == "magenta":
        print("", "magenta")
    elif color == "black":
        print("", "black")
    elif color == "white":
        print("", "white")