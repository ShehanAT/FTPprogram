from PyQt5.QtWidgets import (QMessageBox)
from pysftp import paramiko
import pysftp, os


def remoteToLocalTransfer(self, remoteFile):
    if remoteFile == []:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No file selected to file transfer. Make sure you double-click the file to transfer!")
        errorMessage.exec_()
        return 
    try: 
        if self.currentLocalPath[-1] == "/":
            size = len(self.currentLocalPath)
            self.currentLocalPath = self.currentLocalPath[:size - 1]
        remoteFileName = remoteFile.text().split(" -")[0]
        newLocalArr = remoteFileName.split("/")
        arrLength = len(newLocalArr)
        i = 0
        while i < arrLength:
            if newLocalArr[i] == "":
                del(newLocalArr[i])
                arrLength -= 1
                continue 
            i += 1
        if self.currentLocalPath[-1] != "\\":
            self.currentLocalPath += "\\"
        newLocalFileName = newLocalArr[-1]
        with self.connection.cd(self.currentRemotePath):
            self.connection.get(remoteFileName, self.currentLocalPath + newLocalFileName)
            # self.updateLocalFiles()
            updateLocalFiles(self)
            showFileTransferSuccessMsg(self)
    except IsADirectoryError:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
        errorMessage.exec_()
    except PermissionError:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission Denied for file transfer")
        errorMessage.exec_()
    except FileNotFoundError:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No such file")
        errorMessage.exec_()
    except OSError:
        tracebackString = traceback.print_exc()
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
        errorMessage.exec_()
    except Exception:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Ran into error while file transfering")     
        errorMessage.exec_() 

def updateLocalFiles(self):
    self.LocalFilesList.clear()
    localFiles = os.scandir(self.currentLocalPath)
    self.createLocalFilesList(localFiles)

def showFileTransferSuccessMsg(self):
    transfer_success_msg = QMessageBox()
    transfer_success_msg.setWindowTitle("File Transferred")
    transfer_success_msg.setText("File transferred successfully!")
    transfer_success_msg.setIcon(QMessageBox.Information)
    transfer_success_msg.exec_()
