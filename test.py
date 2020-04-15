from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout 

app = QApplication([])
button = QPushButton('Click')

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()
