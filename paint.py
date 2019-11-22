from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 

from MainWindow import Ui_MainWindow 

import os 
import random 
import types 

BRUSH_MULT = 3
SPRAY_PAINT_MULT = 5
SPRAY_PAINT_N = 100

COLORS = [

]

FONT_SIZES = [

]

MODES = [
    
]

CANVAS_DIMENSIONS = 600, 400 

STAMP_DIR = "./stamps"
STAMPS = [os.path.join(STAMP_DIR, f) for f in os.listdir(STAMP_DIR)]

SELECTION_PEN = QPen(QColor(0xff, 0xff, 0xff), 1, Qt.Dashline)
PREVIEW_PEN = QPen(QColor(0xff, 0xff, 0xff), 1, Qt.SolidLine)

def build_font(config):
    """
    Construct a complete font from the configuration options
    To be continued
    """
