from PyQt5.QtWidgets import (QMessageBox)
from pysftp import paramiko
import pysftp

def startFTP(self, hostname, username, password):
    self.clearAllData()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try: 
        self.connection = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts)
        self.getLocalFileList()
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
            self.updateLocalFiles()
            self.showFileTransferSuccessMsg()
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

def localToRemoteTransfer(self, localFile):
    if localFile == []:
        errorMessage = QMessageBox(QMessageBox.Critical, "Error", "No file selected to file transfer. Make sure you double-click the file to transfer!")
        errorMessage.exec_()
        return 
    with self.connection.cd(self.currentRemotePath):
        try:
            localFileName = localFile.text().split(" -")[0]
            self.connection.put(localFileName) 
            self.updateRemoteFiles()
            self.showFileTransferSuccessMsg()
        except IsADirectoryError:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "The selected file is a directory, please select a file instead.")
            errorMessage.exec_()
        except PermissionError: 
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Permission denied for file transfer")
            errorMessage.exec_()
        except Exception:
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Ran into an error while file transfering")