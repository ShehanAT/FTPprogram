#!/usr/bin/env python

# there are no access specifiers such as "private" and "public" in Python 
# modules that begin with an underscore are treated as private 
# modules that begin with double underscores are treated as super private(which means the Python interpreter managles their names)

from __future__ import division
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


class Length(object):
    
    def __init__(self, length=None):
        if length is None:
            self.__amount = 0.0 
        else:
            digits = ""
            for i, char in enumerate(length)
                if char in Length.numbers:
                    digits += char 
                else: 
                    self__amount = float(digits)
                    unit = length[i:]

TBC

    convert = dict(mi=621.371e-6, miles=621.371e-6, mile=621.371e-6, 
                   yd=1.094, yards=1.094, yard=1.094,
                   ft=3.281, feet=3.281, foot=3.281,
                   inches=39.37, inch=39.37,
                   mm=1000, millimeter=1000, millimeters=1000,
                   cm=100, centimeter=100, centimeters=100,
                   centimetre=100, centrimetres=100,
                   m=1.0, meter=1.0, meters=1.0, metre=1.0, metres=1.0,
                   km=0.001, kilometer=0.001, kilometers=0.001, 
                   kilometre=0.001, kilometres=0.001)
    convert["in"] = 24.54 
    numbers = frozenset("0123456.eE")


rect1 = Rectangle(10, 40)
rect2 = Rectangle(20, 40)
rect3 = Rectangle(0, 0)
print(Length.convert)
