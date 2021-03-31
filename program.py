from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import os, pathlib, sys, traceback, pysftp
from pysftp import paramiko
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
    QGridLayout, QLabel, QStyleFactory, QListWidget, 
    QListWidgetItem, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QBrush
from local_transfer import startFTP, localToRemoteTransfer, getLocalFileList
from remote_transfer import remoteToLocalTransfer
from delete import deleteFile, showDeleteFileSuccessMsg
from draw import (createTopTextBoxes, createBottomCenterBox, createDeleteButton, 
                    createNotificationBox, createBottomLeftBox, createBottomRightBox)

class Program(QMainWindow):
    def __init__(self, parent=None):
        super(Program, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("FTP Program")
        self.setFixedWidth(1500)
        self.setFixedHeight(750)
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        self.LocalFilesList = QListWidget(self)
        self.RemoteFilesList = QListWidget(self)
        self.currentRemotePath = "/"  
        self.currentLocalPath = "\\"  
        self.currentFile = "/"  
        self.currentFileList = ""
        self.localSelectedFile = []
        self.hostName = ''
        self.username = ''
        self.password = ''

        createNotificationBox(self)
        createBottomLeftBox(self)
        createBottomRightBox(self)
        createBottomCenterBox(self)
        createTopTextBoxes(self)
        createDeleteButton(self)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        
        # eventlisteners 
        self.quickConnectButton.clicked.connect(lambda:startFTP(self, self.hostnameTextBox.text(), self.usernameTextBox.text(), self.passwordTextBox.text()))
        self.rightArrowButton.clicked.connect(lambda:remoteToLocalTransfer(self, self.remoteSelectedFile))
        self.leftArrowButton.clicked.connect(lambda:localToRemoteTransfer(self, self.localSelectedFile))
        self.deleteButton.clicked.connect(lambda:deleteFile(self))

        self.directoryIcon = QIcon(self.currentDir + "/icons/directory.png")
        self.fileIcon = QIcon(self.currentDir + "/icons/file.png")
    
        # Misc

    def clearAllData(self):
        self.LocalFilesList.clear()
        self.RemoteFilesList.clear()
        self.currentLocalPath = "\\"
        self.currentRemotePath = "/"
        self.currentFile = ""
        self.currentFileList = ""

    def changePalette(self):
        if(self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

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
            self.RemoteFilesList.clear() 
            remoteFiles = self.connection.listdir_attr("./")
            remoteDir = self.connection.normalize(".")
            if self.currentRemotePath == "/":
                self.currentRemotePath = self.connection.pwd + self.currentRemotePath
        self.createRemoteFilesList(remoteFiles)
        return True 

    def createRemoteFilesList(self, remoteFiles):
        QListWidgetItem("..", self.RemoteFilesList).setIcon(self.directoryIcon)
        for file in remoteFiles:
            fileType = file.st_mode // 10000
            if fileType == 1:
                QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(self.directoryIcon)
                self.RemoteFilesList.findItems(self.currentRemotePath + file.filename + " - " + str(file.st_size), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            elif fileType == 3:
                QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(self.fileIcon)

    def createLocalFilesList(self, localFiles):
        QListWidgetItem("..", self.LocalFilesList).setIcon(self.directoryIcon)
        for file in localFiles:
            fileType = list(file.stat())[0] // 10000
            if fileType == 1:
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.directoryIcon)
                self.LocalFilesList.findItems(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            if fileType == 3:
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.fileIcon)

    def localFileSelectionChangedSingleClick(self):
        self.currentFile = self.LocalFilesList.selectedItems()[0]
        self.currentFileList = "Local"
   
    def localFileSelectionChanged(self):
        self.localSelectedFile = self.LocalFilesList.selectedItems()[0]
        item = self.localSelectedFile
        if item.text() == "..":
            getLocalFileList(self, "..")
            self.localSelectedFile = ""
        else:
            if item.background().color().getRgb() == (100, 100, 150, 255):
                # selection is dir, switch dirs 
                if self.currentLocalPath == "/":
                    self.currentLocalPath = item.text().split(" -")[0] + self.currentLocalPath
                else:
                    self.currentLocalPath = item.text().split(" -")[0] + "\\"
                self.LocalFilesList.clear()
                localFiles = os.scandir(self.currentLocalPath)
                self.createLocalFilesList(localFiles)
                self.localSelectedFile = ""   
   
    def remoteFileSelectionChangedSingleClick(self):
        self.currentFile = self.RemoteFilesList.selectedItems()[0]
        self.currentFileList = "Remote"

    def remoteFileSelectionChanged(self):
        self.remoteSelectedFile = self.RemoteFilesList.selectedItems()[0]
        item = self.remoteSelectedFile
        if item.text() == "..":
            self.getRemoteFileList("..")
            self.remoteSelectedFile = ""
        else:
            if item.background().color().getRgb() == (100, 100, 150, 255):
                if self.currentRemotePath == "/":
                    self.currentRemotePath = item.text().split(" -")[0] + self.currentRemotePath
                else:
                    self.currentRemotePath = item.text().split(" -")[0] + "/"
                with self.connection.cd(self.currentRemotePath):
                    self.RemoteFilesList.clear()
                    QListWidgetItem("..", self.RemoteFilesList).setIcon(self.directoryIcon)
                    for file in self.connection.listdir_attr():
                        fileType = file.st_mode // 10000
                        if fileType == 1:
                            QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(self.directoryIcon)
                            self.RemoteFilesList.findItems(self.currentRemotePath + file.filename + " - " + str(file.st_size), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
                        if fileType == 3:
                            QListWidgetItem(self.currentRemotePath + file.filename + " - " + str(file.st_size) , self.RemoteFilesList).setIcon(self.fileIcon)
                self.remoteSelectedFile = ""