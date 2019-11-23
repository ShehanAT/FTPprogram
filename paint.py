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
    font = config['font']
    font.setPointSize(config['fontsize'])
    font.setBold(config['bold'])
    font.setItalic(config['italic'])
    font.setUnderline(config['underline'])
    return font 

class Canvas(QLabel):
    mode = 'rectangle'

    primary_color = QColor(Qt.black)
    secondary_color = None 

    primary_color_updated = pyqtSignal(str)
    secondary_color_updated = pyqtSignal(str)

    def initalize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)
        self.reset()