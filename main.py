from PyQt5.QtWidgets import QApplication
from program import Program
import sys 

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gallery = Program()
    gallery.show()
    sys.exit(app.exec_())
