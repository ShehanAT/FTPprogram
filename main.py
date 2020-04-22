from PyQt5.QtWidgets import QApplication
from program import Program

if __name__ == '__main__':
    import sys 

    app = QApplication(sys.argv)
    gallery = Program()
    gallery.show()
    sys.exit(app.exec_())
