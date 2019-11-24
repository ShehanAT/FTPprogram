#!/usr/bin/env python 
"""
A simple window in PyQt5
Author: Jan Bodnar 

"""

import sys 
from PyQt5.QtWidgets import QApplication, QWidget 
from PyQt5.QtCore import *
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Whatever I want')
    w.show()

    x = str()
    y = QDate()

    sys.exit(app.exec_())
