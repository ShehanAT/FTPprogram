from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import os, pathlib, sys, traceback, pysftp, time
from datetime import datetime
from pysftp import paramiko
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
    QGridLayout, QLabel, QStyleFactory, QListWidget, 
    QListWidgetItem, QMainWindow, QTreeWidget, QTreeWidgetItem, QMessageBox)
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
        self.LocalFilesList = QTreeWidget(self)
        self.RemoteFilesList = QTreeWidget(self)
        self.currentRemotePathLabel = QLabel(self)
        self.currentLocalPathLabel = QLabel(self)
        self.currentRemotePathDisplay = QLabel(self)
        self.currentLocalPathDisplay = QLabel(self)
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

        # Misc
        self.directoryIcon = QIcon(self.currentDir + "/icons/directory.png")
        self.fileIcon = QIcon(self.currentDir + "/icons/file.png")
    
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            startFTP(self, self.hostnameTextBox.text(), self.usernameTextBox.text(), self.passwordTextBox.text())

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
                self.currentRemotePathDisplay.setText(self.currentRemotePath)
                return False 
            self.RemoteFilesList.clear() # clear current list since back navigation is valid
            newRemoteArr.pop()
            newRemotePath = ""
            if len(newRemoteArr) != 0:
                for i in newRemoteArr:
                    newRemotePath = newRemotePath + '/'
                    newRemotePath = newRemotePath + i 
                # self.currentRemotePath = newRemotePath + "/"
                self.currentRemotePath = newRemotePath 
            else:
                newRemotePath = "/"
                self.currentRemotePath = newRemotePath 
            remoteFiles = self.connection.listdir_attr(self.currentRemotePath)
        else: 
            self.RemoteFilesList.clear() 
            # remoteDir = self.connection.normalize(".")
            if self.currentRemotePath == "/":
                remoteFiles = self.connection.listdir_attr("./")
                self.currentRemotePath = self.connection.pwd 
            else:
                remoteFiles = self.connection.listdir_attr(self.currentRemotePath)
        self.currentRemotePathDisplay.setText(self.currentRemotePath)
        self.createRemoteFilesList(remoteFiles)
        return True 

    def createRemoteFilesList(self, remoteFiles):
        remote_list = []
        self.RemoteFilesList.addTopLevelItem(QTreeWidgetItem(["..", "  ", "  "]))
        for file in remoteFiles:
            fileType = file.st_mode // 10000
            file_name = file.filename 
            date_modified = datetime.fromtimestamp(file.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            file_size = str(file.st_size) 
            if fileType == 1: # for dir 
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.directoryIcon)
                for i in range(0, self.RemoteFilesList.columnCount()):
                    item_file.setBackground(i, QColor(100,100,150))
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.RemoteFilesList.addTopLevelItem(item_file)
            elif fileType == 3: # for files
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.fileIcon)
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.RemoteFilesList.addTopLevelItem(item_file)

    def createLocalFilesList(self, localFiles):
        self.LocalFilesList.addTopLevelItem(QTreeWidgetItem(["..", " ", "  "]))
        try: 
            for file in localFiles:
                fileType = list(file.stat())[0] // 10000
                stat_file = os.stat(file)
                date_modified = datetime.fromtimestamp(os.path.getmtime(file.path)).strftime("%Y-%m-%d %H:%M:%S")
                file_name = file.name
                file_size = str(stat_file.st_size)
                if fileType == 1:
                    item_file = QTreeWidgetItem()
                    item_file.setIcon(0, self.directoryIcon)
                    item_file.setStatusTip(0, "d")
                    for n, i in enumerate((file_name, date_modified, file_size)):
                        item_file.setText(n, i)
                    self.LocalFilesList.addTopLevelItem(item_file)
                elif fileType == 3:
                    item_file = QTreeWidgetItem()
                    item_file.setIcon(0, self.fileIcon)
                    for n, i in enumerate((file_name, date_modified, file_size)):
                        item_file.setText(n, i)
                    self.LocalFilesList.addTopLevelItem(item_file)
            self.currentLocalPathDisplay.setText(self.currentLocalPath)
        except FileNotFoundError as e:
            self.currentLocalPathDisplay.setText(self.currentLocalPath)
            error_message = QMessageBox()
            error_message.setWindowTitle("File not found error")
            error_message.setText(str(e))
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()

    def localFileSelectionChangedSingleClick(self):
        self.currentFile = self.LocalFilesList.selectedItems()[0]
        self.currentFileList = "Local"
   
    def localFileSelectionChanged(self):
        self.localSelectedFile = self.LocalFilesList.selectedItems()[0]
        item = self.localSelectedFile
        if item.text(0) == "..":
            getLocalFileList(self, "..")
            self.localSelectedFile = ""
        else:
            if item.statusTip(0) == 'd':
                # selection is dir, switch dirs 
                if self.currentLocalPath == "/":
                    self.currentLocalPath = item.text(0).split(" -")[0] + self.currentLocalPath
                else:
                    if self.currentLocalPath.endswith("\\"):
                    # removing the 'def\\' in path: '\\abc\def\\' 
                        if self.currentLocalPath == "C:\\\\":
                            self.currentLocalPath = "C:"
                        else:
                            self.currentLocalPath = self.currentLocalPath[:-1] 
                    self.currentLocalPath += "\\" + item.text(0)
                try:
                    localFiles = os.scandir(self.currentLocalPath)
                except PermissionError as e:
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Permission Error")
                    error_message.setText(str(e))
                    error_message.setIcon(QMessageBox.Critical)
                    error_message.exec_()

                    localArr = list(os.path.split(self.currentLocalPath))
                    self.currentLocalPath = localArr[0]
                    return 
                self.LocalFilesList.clear()
                self.createLocalFilesList(localFiles)
                self.localSelectedFile = ""   
   
    def remoteFileSelectionChangedSingleClick(self):
        self.currentFile = self.RemoteFilesList.selectedItems()[0]
        self.currentFileList = "Remote"

    def remoteFileSelectionChanged(self):
        self.remoteSelectedFile = self.RemoteFilesList.selectedItems()[0]
        item = self.remoteSelectedFile
        if item.text(0) == "..":
            self.getRemoteFileList("..")
            self.remoteSelectedFile = ""
        else:
            if item.statusTip(0) == "d":
                # selection is dir 
                if self.currentRemotePath == "/":
                    # self.currentRemotePath = item.text(0).split(" -")[0] + self.currentRemotePath
                    self.currentRemotePath += item.text(0)
                else:
                    if self.currentRemotePath.endswith("/"):
                        # removing the 'def/' in path: '/abc/def/'
                        self.currentRemotePath = self.currentRemotePath[:-1]
                    self.currentRemotePath += "/" + item.text(0)
                try:
                    with self.connection.cd(self.currentRemotePath):
                        self.RemoteFilesList.clear()
                        remote_files = self.connection.listdir_attr()
                        self.createRemoteFilesList(remote_files)
                except PermissionError as e:
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Permission Error")
                    error_message.setText(str(e))
                    error_message.setIcon(QMessageBox.Critical)
                    error_message.exec_()

                    remoteArr = list(os.path.split(self.currentRemotePath))
                    self.currentRemotePath = remoteArr[0] 
                except Exception as e:
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Remote File System Error")
                    error_message.setText(str(e))
                    error_message.setIcon(QMessageBox.Critical)
                    error_message.exec_()

                    remoteArr = list(os.path.split(self.currentRemotePath))
                    self.currentRemotePath = remoteArr[0] 
                    
    def createRemoteFilesList(self, remote_files):
        self.RemoteFilesList.addTopLevelItem(QTreeWidgetItem(["..", " ", " "]))   
        for file in remote_files:
            fileType = file.st_mode // 10000
            file_name = file.filename
            file_size = str(file.st_size)
            date_modified = datetime.fromtimestamp(file.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            if fileType == 1:
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.directoryIcon)
                item_file.setStatusTip(0, 'd')
                # for i in range(0, self.RemoteFilesList.columnCount()):
                #     item_file.setBackground(i, QColor(100,100,150))
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.RemoteFilesList.addTopLevelItem(item_file)
            if fileType == 3:
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.fileIcon)
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.RemoteFilesList.addTopLevelItem(item_file)
        self.remoteSelectedFile = ""
        self.currentRemotePathDisplay.setText(self.currentRemotePath)