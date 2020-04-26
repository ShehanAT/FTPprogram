from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import pysftp
import sys 
import traceback
import os 
from pysftp import paramiko
from waitingSpinner import QtWaitingSpinner
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, 
    QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, 
    QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QToolButton, QMessageBox, QFrame, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush
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
    
        self.createNotificationBox()
        self.createBottomLeftBox()
        self.createBottomRightBox()
        self.createBottonCenterBox()
        self.createTopTextBoxes()
        self.createProgressBar()

        self.currentRemotePath = "/"   
        self.currentLocalPath = "/"    
        self.startFTP("138.197.157.45", "root", "Nanderlone123")
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
        try: 
            self.connection = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts)
            self.getLocalFileList("/Users/shehan/")
            self.getRemoteFileList()
            self.notificationLabel.setText("Please select file to transfer and click the arrow buttons...")
            self.rightArrowButton.setEnabled(True)
            self.leftArrowButton.setEnabled(True)
        except paramiko.ssh_exception.SSHException:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "SSH Failed! Unable to connect to " + hostname)
            errorMessage.exec_()
        except paramiko.ssh_exception.AuthenticationException:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Authentication Failed! Please make sure to enter a valid hostname, username and password")
            errorMessage.exec_()


    def updateRemoteFiles(self):
        remoteFiles = self.connection.listdir("./")
        for file in remoteFiles:
            if len(self.RemoteFilesList.findItems(file, Qt.MatchContains)) == 0:
                QListWidgetItem(file, self.RemoteFilesList)

    def updateLocalFiles(self):
        localPath = "/Users/shehan/"
        localFiles = os.listdir(localPath)

        for file in localFiles:
            if len(self.LocalFilesList.findItems(file, Qt.MatchContains)) == 0:
                QListWidgetItem("/Users/shehan/" + file, self.LocalFilesList)
        
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

    def createNotificationBox(self):
        self.notificationLabel = QLabel(self)
        self.notificationLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.notificationLabel.setText("Please enter remote credentials to continue...")
        self.notificationLabel.setAlignment(Qt.AlignTop)
        self.notificationLabel.resize(400, 20)
     

    def createBottomLeftBox(self):
        self.RemoteFilesList = QListWidget(self)
        self.RemoteFilesList.move(20, 110)
        self.RemoteFilesList.resize(280, 280)
        self.remoteSelectedFile = [] 

        self.RemoteFilesLabel = QLabel(self)
        self.RemoteFilesLabel.setText("Remote Files Section:\n{file} - {size}")
        self.RemoteFilesLabel.move(20, 70)
        self.RemoteFilesList.itemDoubleClicked.connect(self.remoteFileSelectionChanged)
        # self.RemoteFilesList.itemSelectionChanged.connect(self.remoteFileSelectionChanged)

    def changeLocalDir(self):
        self.localFileBrowser = QFileDialog().getExistingDirectory(self, "Change current directory", os.path.expanduser("~"), QFileDialog.ShowDirsOnly)
        self.getLocalFileList(self.localFileBrowser + "/")

    def createBottomRightBox(self):
        self.changeLocalDirBtn = QPushButton(self)
        self.changeLocalDirBtn.setDefault(True)
        self.changeLocalDirBtn.move(700,70)
        self.changeLocalDirBtn.resize(150, 40)
        self.changeLocalDirBtn.setText("Change Local Dir")
        self.changeLocalDirBtn.setStyleSheet("background-color: #fff; color: black; border: 1px solid blue;")
        self.changeLocalDirBtn.clicked.connect(lambda:self.changeLocalDir())
        
        self.LocalFilesList = QListWidget(self)
        self.LocalFilesList.move(400, 110)
        self.LocalFilesList.resize(280, 280)
        self.localSelectedFile = []

        self.LocalFilesLabel = QLabel(self)
        self.LocalFilesLabel.setText("Local Files Section:\n{file} - {size}") 
        self.LocalFilesLabel.move(400, 70)
        self.LocalFilesList.itemDoubleClicked.connect(self.localFileSelectionChanged)

    def getLocalFileList(self, localPath):
        if localPath == "..":
            newLocalArr = self.currentLocalPath.split("/")
            arrLength = len(newLocalArr)
            i = 0
            while i < arrLength:
                if newLocalArr[i] == "":
                    del(newLocalArr[i])
                    arrLength -= 1
                    continue
                i += 1 
            if len(newLocalArr) == 0:
                # self.currentLocalPath is "/"
                return False 
            self.LocalFilesList.clear()
            newLocalArr.pop()
            newLocalPath = ""
            if len(newLocalArr) != 0:
                for i in newLocalArr:
                    newLocalPath = newLocalPath + '/'
                    newLocalPath = newLocalPath + i 
            localPath = newLocalPath[:-1]
            self.currentLocalPath = "/"
            self.currentLocalPath = newLocalPath + self.currentLocalPath
            localFiles = os.scandir(self.currentLocalPath)
        else:  
            localFiles = os.scandir("./")
            self.currentLocalPath = os.getcwd() + self.currentLocalPath
        # create back button 
        QListWidgetItem("..", self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
        for file in localFiles:
            fileType = list(file.stat())[0] // 10000
            if fileType == 1:
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                self.LocalFilesList.findItems(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            elif fileType == 3:
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/file.png"))
        return True 
    def getRemoteFileList(self, *args):
        if args:
            newRemoteArr = self.currentRemotePath.split("/")
            arrLength = len(newRemoteArr)
            i = 0
            while i < arrLength:
                if newRemoteArr[i] == "":
                    del(newRemoteArr[i])
                    arrLength -= 1
                    continue
                i += 1 
            if len(newRemoteArr) == 0:
                # self.currentRemotePath is "/"
                return False 
            self.RemoteFilesList.clear() # clear current list since back navigation is valid
            newRemoteArr.pop()
            newRemotePath = ""
            if len(newRemoteArr) != 0:
                for i in newRemoteArr:
                    newRemotePath = newRemotePath + '/'
                    newRemotePath = newRemotePath + i 
            remotePath = newRemotePath[:-1]
            self.currentRemotePath = "/"
            self.currentRemotePath = newRemotePath + self.currentRemotePath
            remoteFiles = self.connection.listdir_attr(self.currentRemotePath)
            
        else:  
            remoteFiles = self.connection.listdir_attr("./")
            remoteDir = self.connection.normalize(".")
            self.currentRemotePath = self.connection.pwd + self.currentRemotePath
        QListWidgetItem("..", self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
        for file in remoteFiles:
            fileType = file.st_mode // 10000
            if fileType == 1:
                QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                self.RemoteFilesList.findItems(self.currentRemotePath + file.filename + " - " + str(file.st_size), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            elif fileType == 3:
                QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/file.png"))
        return True 
    def localFileSelectionChanged(self):
        self.localSelectedFile.append(self.LocalFilesList.selectedItems())
        item = self.localSelectedFile[0][0]
        if item.text() == "..":
            self.getLocalFileList("..")
            self.localSelectedFile = []
        else:
            if item.background().color().getRgb() == (100, 100, 150, 255):
                # selection is dir, switch dirs 
                if self.currentLocalPath == "/":
                    self.currentLocalPath = item.text().split(" -")[0] + self.currentLocalPath
                else:
                    self.currentLocalPath = item.text().split(" -")[0] + "/"
                self.LocalFilesList.clear()
                QListWidgetItem("..", self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                try:
                    for file in os.scandir(self.currentLocalPath):
                        fileType = list(file.stat())[0] // 10000
                        if fileType == 1:
                            QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                            self.LocalFilesList.findItems(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
                        if fileType == 3:
                            QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/file.png"))
                except PermissionError:
                    errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission Denied for file transfer")
                    errorMessage.exec_()
            self.localSelectedFile = []    

    def remoteFileSelectionChanged(self):
        self.remoteSelectedFile.append(self.RemoteFilesList.selectedItems())
        if self.remoteSelectedFile[0][0].text() == "..":
            self.getRemoteFileList("..")
            self.remoteSelectedFile = []
        else:
            item = self.remoteSelectedFile[0][0]
            if item.background().color().getRgb() == (100, 100, 150, 255):
                if self.currentRemotePath == "/":
                    self.currentRemotePath = item.text().split(" -")[0] + self.currentRemotePath
                else:
                    self.currentRemotePath = item.text().split(" -")[0] + "/"
                with self.connection.cd(self.currentRemotePath):
                    self.RemoteFilesList.clear()
                    QListWidgetItem("..", self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                    for file in self.connection.listdir_attr():
                        fileType = file.st_mode // 10000
                        if fileType == 1:
                            QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/directory.png"))
                            self.RemoteFilesList.findItems(self.currentRemotePath + file.filename + " - " + str(file.st_size), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
                        if fileType == 3:
                            QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(QIcon("/Users/shehan/Documents/FTPprogram/icons/file.png"))
            self.remoteSelectedFile = []

    def localToRemoteTransfer(self, localFileName):
        with self.connection.cd("/root"):
            try:
                self.connection.put(localFileName[0].text()) 
                self.updateRemoteFiles()
            except IsADirectoryError:
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
                errorMessage.exec_()
        
    def remoteToLocalTransfer(self, remoteFileName):
        # try: 
        with self.connection.cd(self.currentRemotePath):
            self.connection.get(remoteFileName[0].text(), "/Users/shehan/" + remoteFileName[0].text())
        # except IsADirectoryError:
        #     errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
        #     errorMessage.exec_()
        # except PermissionError:
        #     errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission Denied for file transfer")
        #     errorMessage.exec_()
        # except FileNotFoundError:
        #     errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No such file")
        #     errorMessage.exec_()
        # except OSError:
        #     tracebackString = traceback.print_exc()
        #     errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
        #     errorMessage.exec_()
        self.updateLocalFiles()

       

    def createBottonCenterBox(self):
        self.rightArrowButton = QToolButton(self)
        self.rightArrowButton.setIcon(QIcon(os.getcwd() + "/icons/right.png" ))
        self.rightArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.rightArrowButton.setCursor(Qt.ArrowCursor)
        self.rightArrowButton.resize(45, 45)
        self.rightArrowButton.move(330, 100)
        self.rightArrowButton.clicked.connect(lambda:self.remoteToLocalTransfer(self.remoteSelectedFile[0]))
        self.rightArrowButton.setEnabled(False)

        self.leftArrowButton = QToolButton(self)
        self.leftArrowButton.setIcon(QIcon(os.getcwd() + "/icons/left.png"))
        self.leftArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
        self.leftArrowButton.setCursor(Qt.ArrowCursor)
        self.leftArrowButton.resize(45, 45)
        self.leftArrowButton.move(330, 165)
        self.leftArrowButton.clicked.connect(lambda:self.localToRemoteTransfer(self.localSelectedFile[0]))
        self.leftArrowButton.setEnabled(False)

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
        self.quickConnectButton.setStyleSheet('QPushButton {background-color: #fff; color: black; border: 1px solid blue;}')
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
