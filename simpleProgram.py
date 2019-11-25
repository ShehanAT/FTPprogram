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

  

    one = [9, 36, 16, 25, 4, 1]
    two = dict(india=9, golf=17, juliet=5, foxtrot=61, hotel=8)
    three = {11: "lima", 13: "kilo", 12: "mike"}
    two[100] = "Shehan"

    now = QDate.currentDate()
    never = QDate()
    print(bool(now), bool(never)) # bool(never) returns false
   # print(v1, v2)
    
    # Python uses indentation to signify its block structure
    # 4 spaces are recommended for indentation
    x = 5
    if x == 5:
        pass # do nothing in this case
    if x == 5: pass # this format is also valid
    # whenever a colon is used the next statement can be on the same line
    # there is no built-in switch/case statements in Python

    print("x is zero or positive" if x >= 0 else "x is negetive")
    # This is Python's ternary operator 

    for char in "aeiou":
        print("%s=%d" % (char, ord(char))) # ord(char) prints ascii character

    # semi colons are not used in python, newlines are the statement seperators 
    #sys.exit(app.exec_())
