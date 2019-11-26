#!/usr/bin/env python 
"""
A simple window in PyQt5
Author: Jan Bodnar 

"""

import sys 
from PyQt5.QtWidgets import QApplication, QWidget 
from PyQt5.QtCore import *

if __name__ == '__main__':
    #app = QApplication(sys.argv)

   # w = QWidget()
   # w.resize(250, 150)
   # w.move(300, 300)
   # w.setWindowTitle('Whatever I want')
   # w.show()

  

    # one = [9, 36, 16, 25, 4, 1]
    # two = dict(india=9, golf=17, juliet=5, foxtrot=61, hotel=8)
    # three = {11: "lima", 13: "kilo", 12: "mike"}
    # two[100] = "Shehan"

    # now = QDate.currentDate()
    # never = QDate()
    # print(bool(now), bool(never)) # bool(never) returns false
   # print(v1, v2)
    
    # Python uses indentation to signify its block structure
    # 4 spaces are recommended for indentation
    # x = 5
    # if x == 5:
    #     pass # do nothing in this case
    # if x == 5: pass # this format is also valid
    # whenever a colon is used the next statement can be on the same line
    # there is no built-in switch/case statements in Python

    # print("x is zero or positive" if x >= 0 else "x is negetive")
    # This is Python's ternary operator 

    # for char in "aeiou":
    #     print("%s=%d" % (char, ord(char))) # ord(char) prints ascii character

    # semi colons are not used in python, newlines are the statement seperators 
    #sys.exit(app.exec_())

    # for x in ( x for x in range(50) if x % 5 == 0):
    #     print(x) # prints all multiples of 5 from 0 to 50


    def simpleFunction(param1, param2):
        print("Welcome to simple function")

    def frange(start, stop, inc=1): # inc=1 is a default argument 
        result = []
        while start < stop:
            result.append(start)
            start += inc 
        return result  

    def simplify(text, space="\t\r\n\f", delete=""):
        result = []
        word = ""
        for char in text:
            if char in delete:
                continue 
            elif char in space:
                if word:
                    result.append(word)
                    word = ""
            else:
                word += char 
        if word:
            result.append(word)
        return " ".join(result) # returns array with all element concatenated 
    # Python does not allow a default argument parameter to be preceded by 
    # a normal parameter, so ```frange(start=0.5, stop)``` is illegal 
    # Python does not allow overloaded functions  
    print(simplify(" this    and \n that\t too"))