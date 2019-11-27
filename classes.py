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
class Trapezoid(object):
    def __init__(self, width, height):
        self.width = width 
        self.height = height 

    def _area(self):
        return self.width * self.height 
    def getArea(self):
        return self.area 
    
    area = property(fget=_area)
trap1 = Trapezoid(20, 34)
rect1 = Rectangle(20, 40)
print(trap1.getArea())