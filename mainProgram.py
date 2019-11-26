#!/usr/bin/env 
import functools
import sys 

def hello():
    print("Hello")
def world():
    print("World")
def action(button):
    print("You press button %s" % button)
def main():
    hello()
    world()

# buttonOneFunc = functools.partial(action, "One") #
# buttonOneFunc() # prints result of action("One") 
# try/catch block in Python 
try:
    print("Suffering")
except Exception:
    print("Is Beautiful")
else:
    print("Right?")
main()