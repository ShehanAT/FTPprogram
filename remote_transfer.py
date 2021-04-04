from PyQt5.QtWidgets import (QMessageBox)
from pysftp import paramiko
import pysftp, os, logging

logger = logging.getLogger("FTP-program")
def remoteToLocalTransfer(self, remoteFile):
    if remoteFile == []:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No file selected to file transfer. Make sure you double-click the file to transfer!")
        errorMessage.exec_()
        return 
    try: 
        if self.currentLocalPath[-1] == "/":
            size = len(self.currentLocalPath)
            self.currentLocalPath = self.currentLocalPath[:size - 1]
        remoteFileName = remoteFile.text(0)
        if self.currentLocalPath[-1] != "\\":
            self.currentLocalPath += "\\"
        newLocalFileName = remoteFileName 
        with self.connection.cd(self.currentRemotePath):
            localPathDest = self.currentLocalPath + newLocalFileName 
            self.connection.get(remoteFileName, localPathDest)
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
    except Exception as e:
        logger.error(e)
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", str(e))     
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
