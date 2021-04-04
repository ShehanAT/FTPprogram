from PyQt5.QtWidgets import (QMessageBox, QApplication)
from pysftp import paramiko
import pysftp, os, logging
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QListWidget, 
    QListWidgetItem, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt


logger = logging.getLogger('FTP-Program')
def startFTP(self, hostname, username, password, public_key=False):
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
    except paramiko.ssh_exception.SSHException as e:
        if hostname == "":                    
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "SSH Failed! Hostname field cannot be empty!")
            errorMessage.exec_()
        else:
            logger.error(e)
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
    self.notificationLabel.setText("Loading...")
    QApplication.setOverrideCursor(Qt.WaitCursor)
    if localFile == []:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No file selected to file transfer. Make sure you double-click the file to transfer!")
        errorMessage.exec_()
        return 
    with self.connection.cd(self.currentRemotePath):
        try:
            localFilePath = self.currentLocalPath + "\\" + localFile.text(0)
            self.connection.put(localFilePath) 
            updateRemoteFiles(self)
            QApplication.restoreOverrideCursor()
            showFileTransferSuccessMsg(self)
        except IsADirectoryError:
            QApplication.restoreOverrideCursor()
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
            errorMessage.exec_()
        except PermissionError: 
            QApplication.restoreOverrideCursor()
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission denied for file transfer")
            errorMessage.exec_()
        except Exception:
            QApplication.restoreOverrideCursor()
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Ran into an error while file transfering")
    self.notificationLabel.setText("")

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
            self.currentLocalPathDisplay.setText(self.currentLocalPath)
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
        self.currentLocalPath = os.getcwd()

    back_button = QTreeWidgetItem(["..", " ", " "])
    self.LocalFilesList.addTopLevelItem(back_button)
    for file in localFiles:
        fileType = list(file.stat())[0] // 10000
        stat_file = os.stat(file)
        date_modified = datetime.fromtimestamp(os.path.getmtime(file.path)).strftime("%Y-%m-%d %H:%M:%S")
        if previous_dir and base_dir == False and delete_dir == False:
            # file_name = "\\" + file.name
            file_name = file.name 
            file_size = str(stat_file.st_size)
            if fileType == 1: # for folders
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.directoryIcon)
                item_file.setStatusTip(0, "d")
                # for i in range(0, self.LocalFilesList.columnCount()):
                #     item_file.setBackground(i, QColor(100,100,150))
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.LocalFilesList.addTopLevelItem(item_file)
            elif fileType == 3: # for files
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.fileIcon)
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.LocalFilesList.addTopLevelItem(item_file)
        else: 
            file_name = file.name 
            file_size = str(stat_file.st_size)
            if fileType == 1: # for folders
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.directoryIcon)
                item_file.setStatusTip(0, "d")
                # for i in range(0, self.LocalFilesList.columnCount()):
                #     item_file.setBackground(i, QColor(100,100,150))
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.LocalFilesList.addTopLevelItem(item_file)
            elif fileType == 3: # for files
                item_file = QTreeWidgetItem()
                item_file.setIcon(0, self.fileIcon)
                for n, i in enumerate((file_name, date_modified, file_size)):
                    item_file.setText(n, i)
                self.LocalFilesList.addTopLevelItem(item_file)
    self.currentLocalPathDisplay.setText(self.currentLocalPath)
    self.LocalFilesList.resizeColumnToContents(0)
    return True 

def showFileTransferSuccessMsg(self):
    transfer_success_msg = QMessageBox()
    transfer_success_msg.setWindowTitle("File Transferred")
    transfer_success_msg.setText("File transferred successfully!")
    transfer_success_msg.setIcon(QMessageBox.Information)
    transfer_success_msg.exec_()