from PyQt5.QtWidgets import (QMessageBox)
from pysftp import paramiko
import pysftp, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QListWidget, 
    QListWidgetItem)
from PyQt5.QtCore import Qt



def startFTP(self, hostname, username, password):
    self.clearAllData()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try: 
        self.connection = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts)
        self.hostname = hostname
        self.username = username 
        self.password = password 
        getLocalFileList(self)
        self.getRemoteFileList()
        self.notificationLabel.setText("Double-click on a file and click the arrow buttons to file transfer")
        self.rightArrowButton.setEnabled(True)
        self.leftArrowButton.setEnabled(True)
    except paramiko.ssh_exception.SSHException:
        if hostname == "":                    
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "SSH Failed! Hostname field cannot be empty!")
            errorMessage.exec_()
        else:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "SSH Failed! Connection attempt to host: " + hostname +  " failed!")
            errorMessage.exec_()
    except paramiko.ssh_exception.AuthenticationException:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Authentication Failed! Please make sure to enter a valid hostname, username and password")
        errorMessage.exec_()
    except paramiko.sftp.SFTPError:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "SFTP Error: Garbage package received")
        errorMessage.exec_()
    except pysftp.exceptions.ConnectionException:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Connection Exception: Remote server connection failed! Make sure all fields contain valid information with no additional spaces")
        errorMessage.exec_()



def localToRemoteTransfer(self, localFile):
    if localFile == []:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No file selected to file transfer. Make sure you double-click the file to transfer!")
        errorMessage.exec_()
        return 
    with self.connection.cd(self.currentRemotePath):
        try:
            localFileName = localFile.text().split(" -")[0]
            self.connection.put(localFileName) 
            updateRemoteFiles(self)
            showFileTransferSuccessMsg(self)
        except IsADirectoryError:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
            errorMessage.exec_()
        except PermissionError: 
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission denied for file transfer")
            errorMessage.exec_()
        except Exception:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Ran into an error while file transfering")

def updateRemoteFiles(self):
    self.RemoteFilesList.clear()
    remoteFiles = self.connection.listdir_attr("./")
    self.createRemoteFilesList(remoteFiles)

def getLocalFileList(self, localPath=None, afterDelete=False):
    previous_dir = False 
    base_dir = False 
    delete_dir = False 
    if localPath == "..":
        if self.currentLocalPath.endswith("\\") and self.currentLocalPath != "C:\\":
            # removing the 'def\\' in path: '\\abc\def\\' 
            self.currentLocalPath = self.currentLocalPath[:-1] 
        newLocalArr = list(os.path.split(self.currentLocalPath))
        arrLength = len(newLocalArr)
        i = 0
        while i < arrLength:
            if newLocalArr[i] == "":
                del(newLocalArr[i])
                arrLength -= 1
                continue
            i += 1 
        if len(newLocalArr) == 0:
            # self.currentLocalPath is "\"
            return False 
        self.LocalFilesList.clear()
        newLocalPath = newLocalArr[0]
        self.currentLocalPath = str(newLocalPath)
        localFiles = os.scandir(newLocalPath)
        previous_dir = True
        if self.currentLocalPath == "C:\\":
            base_dir = True  
    elif afterDelete:
        self.currentLocalPathLen = len(self.currentLocalPath)
        localFiles = os.scandir(self.currentLocalPath)
        delete_dir = True 
    else:  
        localFiles = os.scandir("./")
        print(type(self))
        self.currentLocalPath = os.getcwd() + self.currentLocalPath
    # create back button 
    QListWidgetItem("..", self.LocalFilesList).setIcon(self.directoryIcon)
    for file in localFiles:
        fileType = list(file.stat())[0] // 10000
        if previous_dir and base_dir == False and delete_dir == False:
            if fileType == 1: # for folders
                QListWidgetItem(self.currentLocalPath + "\\" + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.directoryIcon)
                self.LocalFilesList.findItems(self.currentLocalPath + "\\" + file.name + " - " + str(list(file.stat())[6]), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            elif fileType == 3: # for files
                QListWidgetItem(self.currentLocalPath + "\\" + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.fileIcon)
        else: 
            if fileType == 1: # for folders
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.directoryIcon)
                self.LocalFilesList.findItems(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]), Qt.MatchContains)[0].setBackground(QColor(100,100,150))
            elif fileType == 3: # for files
                QListWidgetItem(self.currentLocalPath + file.name + " - " + str(list(file.stat())[6]) , self.LocalFilesList).setIcon(self.fileIcon)   
    return True 

def showFileTransferSuccessMsg(self):
    transfer_success_msg = QMessageBox()
    transfer_success_msg.setWindowTitle("File Transferred")
    transfer_success_msg.setText("File transferred successfully!")
    transfer_success_msg.setIcon(QMessageBox.Information)
    transfer_success_msg.exec_()