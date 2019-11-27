#!/usr/bin/env python

# there are no access specifiers such as "private" and "public" in Python 
# modules that begin with an underscore are treated as private 
# modules that begin with double underscores are treated as super private(which means the Python interpreter managles their names)


class Table(object):
    """ This class represents tables"""
    def __init__(self, name, legs=4):
        self.name = name 
        self.legs = legs 

table1 = Table("Sri Lanka")
table2 = Table("India", 1)

class Rectangle(object):
    def __init__(self, width, height):# self is not a required parameter
        self.width = width 
        self.height = height 

    def getWidth(self):
        return self.width 
    
    def setWidth(self, width):
        self.width = width 
    
    def getHeight(self):
        return self.height 

    def setHeight(self, height):
        self.height = height 

    def area(self):
        return self.getWidth() * self.getHeight()

    def __lt__(self, other):
        return self.area() < other.area()
    
    def __eq__(self, other):
        return self.area() == other.area()

    def __gt__(self, other):
        return self.area() > other.area()
    def __repl__(self):# not working 
        return "Rectangle(%d, %d)" % (self.width, self.height)

class Balloon(object):
    unique_colors = set() 

    def __init__(self, color):
        self.color = color 
        Balloon.unique_colors.add(color)
    @staticmethod
    def uniqueColorCount():
        return len(Balloon.unique_colors)
    
    @staticmethod
    def uniqueColors():
        return Balloon.unique_colors.copy()

rect1 = Rectangle(10, 40)
rect2 = Rectangle(20, 40)
rect3 = Rectangle(0, 0)
print(rect1 > rect2)
print(rect1 == rect2)
print(rect1 < rect2)
print(rect1)