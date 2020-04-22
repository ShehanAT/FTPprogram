from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import ftplib 
import pysftp
import sys 
import traceback
import os 


from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, 
    QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, 
    QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QToolButton, QMessageBox)
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon
class Program(QDialog):

    def __init__(self, parent=None):
        super(Program, self).__init__(parent)

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
        # Hostname: 138.197.157.45
        # Username: root 
        # Password: Nanderlone123
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.connection = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts)
        self.getLocalFileList()
        self.getRemoteFileList()


    def updateRemoteFiles(self):
        remoteFiles = self.connection.listdir("./")
        for file in remoteFiles:
            if len(self.RemoteFilesList.findItems(file, Qt.MatchContains)) == 0:
                QListWidgetItem(file, self.RemoteFilesList)

    def updateLocalFiles(self):
        localPath = "/Users/shehan"
        localFiles = os.listdir(localPath)

        for file in localFiles:
            if len(self.LocalFilesList.findItems(file, Qt.MatchContains)) == 0:
                QListWidgetItem(file, self.LocalFilesList)
        
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
        self.RemoteFilesList.move(20, 90)
        self.RemoteFilesList.resize(280, 280)
        self.remoteSelectedFile = [] 

        self.RemoteFilesLabel = QLabel(self)
        self.RemoteFilesLabel.setText("Remote Files Section:")
        self.RemoteFilesLabel.move(20, 70)
        self.RemoteFilesList.itemSelectionChanged.connect(self.remoteFileSelectionChanged)

    def createBottomRightBox(self):
        self.LocalFilesList = QListWidget(self)
        self.LocalFilesList.move(400, 90)
        self.LocalFilesList.resize(280, 280)
        self.localSelectedFile = []

        self.LocalFilesLabel = QLabel(self)
        self.LocalFilesLabel.setText("Local Files Section:") 
        self.LocalFilesLabel.move(400, 70)
        self.LocalFilesList.itemSelectionChanged.connect(self.localFileSelectionChanged)

    def getLocalFileList(self):
        localPath = "/Users/shehan"
        localFiles = os.listdir(localPath)
        for file in localFiles:
            QListWidgetItem(localPath + "/" + file, self.LocalFilesList)

    def getRemoteFileList(self):
        remoteFiles = self.connection.listdir("./")
        for file in remoteFiles:
            QListWidgetItem(file, self.RemoteFilesList)

    def localFileSelectionChanged(self):
        self.localSelectedFile.append(self.LocalFilesList.selectedItems())
    
    def remoteFileSelectionChanged(self):
        self.remoteSelectedFile.append(self.RemoteFilesList.selectedItems())

    def localToRemoteTransfer(self, localFileName):
        with self.connection.cd("/root"):
            try:
                self.connection.put(localFileName[0].text()) 
                self.updateRemoteFiles()
            except IsADirectoryError:
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
                errorMessage.exec_()
        
    def remoteToLocalTransfer(self, remoteFileName):
        with self.connection.cd("/root"):
            try: 
                self.connection.get(remoteFileName[0].text(), "/Users/shehan/" + remoteFileName[0].text())
                self.updateLocalFiles()
            except IsADirectoryError:
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
                errorMessage.exec_()
            except OSError:
                tracebackString = traceback.print_exc()
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
                errorMessage.exec_()

    def createBottonCenterBox(self):
        self.rightArrowButton = QToolButton(self)
        self.rightArrowButton.setIcon(QIcon(os.getcwd() + "/icons/right.png" ))
        self.rightArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.rightArrowButton.setCursor(Qt.ArrowCursor)
        self.rightArrowButton.resize(45, 45)
        self.rightArrowButton.move(330, 100)
        self.rightArrowButton.clicked.connect(lambda:self.remoteToLocalTransfer(self.remoteSelectedFile[0]))

        self.leftArrowButton = QToolButton(self)
        self.leftArrowButton.setIcon(QIcon(os.getcwd() + "/icons/left.png"))
        self.leftArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.leftArrowButton.setCursor(Qt.ArrowCursor)
        self.leftArrowButton.resize(45, 45)
        self.leftArrowButton.move(330, 165)
        self.leftArrowButton.clicked.connect(lambda:self.localToRemoteTransfer(self.localSelectedFile[0]))

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
        self.passwordTextBox.setEchoMode(QLineEdit.Password)
        self.passwordTextBox.move(600, 20)
        self.passwordTextBox.resize(280, 40)
        self.passwordTextBox.setPlaceholderText("Password: ")


        self.quickConnectButton = QPushButton(self)
        self.quickConnectButton.setDefault(True)
        self.quickConnectButton.move(890, 20)
        self.quickConnectButton.resize(150, 40)
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
