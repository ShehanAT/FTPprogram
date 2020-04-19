# from PyQt5.QtCore import QDateTime, Qt, QTimer 
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import ftplib 
import pysftp
import sys 
import os 


from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, 
    QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, 
    QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QToolButton)
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon
class WidgetGallery(QDialog):

    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.createBottomLeftBox()
        self.createBottomRightBox()
        self.createBottonCenterBox()
        self.createTopTextBoxes()
        self.createProgressBar()
        
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        
       


        self.setWindowTitle("Shehan's FTP Program")
        self.changeStyle("Windows")
    def startFTP(self, hostname, username, password):
        # Hostname: sftp://138.197.157.45
        # Username: root 
        # Password: Nanderlone123!
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.connection = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts)
        localFileName = "manage.py"
        manageFile = open(localFileName, "w+")
        remotePath = "manage.py"
        remoteFiles = self.connection.listdir("./")
        for file in remoteFiles:
            QListWidgetItem(file, self.RemoteFilesList)

    def updateRemoteFiles(self):
        remoteFiles = self.connection.listdir("./")
        for file in remoteFiles:
            if len(self.RemoteFilesList.findItems(file, Qt.MatchContains)) == 0:
                QListWidgetItem(file, self.RemoteFilesList)
        
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()
    
    def changePalette(self):
        if(self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        currVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(currVal + (maxVal - currVal) / 100)

    def createBottomLeftBox(self):
        self.RemoteFilesList = QListWidget(self)
        self.RemoteFilesList.move(20, 60)
        self.RemoteFilesList.resize(280, 280)

    def createBottomRightBox(self):
        self.LocalFilesList = QListWidget(self)
        self.LocalFilesList.move(400, 60)
        self.LocalFilesList.resize(280, 280)
        self.localFilesArr = [] 

        self.LocalFilesList.itemSelectionChanged.connect(self.localFileSelectionChanged)
        localPath = "/Users/shehan"
        localFiles = os.listdir(localPath)
        for file in localFiles:
            QListWidgetItem(localPath + "/" + file, self.LocalFilesList)

    def localFileSelectionChanged(self):
        self.localFilesArr.append(self.LocalFilesList.selectedItems())
        for item in self.localFilesArr:
            print(item[0].text())
    
        # self.localFilesArr = []
    
    def localToRemoteTransfer(self, localFileName):
        # cnopts = pysftp.CnOpts()
        # cnopts.hostkeys = None
        # self.connection = pysftp.Connection(host=self.hostname, username=self.username, password=self.password, cnopts=cnopts)
        with self.connection.cd("/root"):
            print("passing123")
            self.connection.put(localFileName[0].text())  
            self.updateRemoteFiles()
            
    def createBottonCenterBox(self):
        self.rightArrowButton = QToolButton(self)
        self.rightArrowButton.setIcon(QIcon(os.getcwd() + "/icons/right.png" ))
        self.rightArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.rightArrowButton.setCursor(Qt.ArrowCursor)
        self.rightArrowButton.resize(45, 45)
        self.rightArrowButton.move(330, 100)

        self.leftArrowButton = QToolButton(self)
        self.leftArrowButton.setIcon(QIcon(os.getcwd() + "/icons/left.png"))
        self.leftArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.leftArrowButton.setCursor(Qt.ArrowCursor)
        self.leftArrowButton.resize(45, 45)
        self.leftArrowButton.move(330, 165)
        self.leftArrowButton.clicked.connect(lambda:self.localToRemoteTransfer(self.localFilesArr[0]))

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio Button 1")
        radioButton2 = QRadioButton("Radio Button 2")
        radioButton3 = QRadioButton("Radio Button 3")
        radioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopTextBoxes(self):
        self.hostnameTextBox = QLineEdit(self)
        self.hostnameTextBox.move(0, 20)
        self.hostnameTextBox.resize(280, 40)
        self.hostnameTextBox.setPlaceholderText("Hostname: ")

        self.usernameTextBox = QLineEdit(self)
        self.usernameTextBox.move(300, 20)
        self.usernameTextBox.resize(280, 40)
        self.usernameTextBox.setPlaceholderText("Username: ")

        self.passwordTextBox = QLineEdit(self)
        self.passwordTextBox.move(600, 20)
        self.passwordTextBox.resize(280, 40)
        self.passwordTextBox.setPlaceholderText("Password: ")

        self.portTextBox = QLineEdit(self)
        self.portTextBox.move(900, 20)
        self.portTextBox.resize(140, 40)
        self.portTextBox.setPlaceholderText("Port:")

        self.quickConnectButton = QPushButton(self)
        self.quickConnectButton.setDefault(True)
        self.quickConnectButton.move(1050, 20)
        self.quickConnectButton.resize(200, 40)
        self.quickConnectButton.setText("Quick Connect")
        self.quickConnectButton.setStyleSheet('QPushButton {background-color: #fff; color: black; border: 1px solid blue}')
        self.hostname = self.hostnameTextBox.text()
        self.username = self.usernameTextBox.text()
        self.password = self.passwordTextBox.text()
        self.quickConnectButton.clicked.connect(lambda:self.startFTP(self.hostnameTextBox.text(), self.usernameTextBox.text(), self.passwordTextBox.text()))
        self.show()

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':
    import sys 

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
