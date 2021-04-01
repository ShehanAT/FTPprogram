from PyQt5.QtWidgets import (QMessageBox)
import os, paramiko
from local_transfer import getLocalFileList


def remoteDelete(self, deleteFilePath):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(self.hostname, username=self.username, password=self.password)
    stdin, stdout, stderr = client.exec_command('rm ' + deleteFilePath)
    client.close()

def showDeleteFileSuccessMsg(self):
    deleteFile_success_msg = QMessageBox()
    deleteFile_success_msg.setWindowTitle("File deleted")
    deleteFile_success_msg.setText("File deleted successfully!")
    deleteFile_success_msg.setIcon(QMessageBox.Information)
    deleteFile_success_msg.exec_()

def deleteFile(self):
    if self.currentFile != "/":
        deleteFile = self.currentFile
        deleteFileName = str(self.currentFile.text())
        deleteFilePath = deleteFileName.split(" -")[0]
        confirmDelete = QMessageBox.question(self, "Confirm Action", "Are you sure you want to delete this file: " + deleteFilePath, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if confirmDelete == QMessageBox.Yes:
            if deleteFile.background().color().getRgb() == (100, 100, 150, 255):
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Cannot delete folders! Only files can be deleted...")
                errorMessage.exec_()
                return 
            if self.currentFileList == "Remote":
                remoteDelete(self, deleteFilePath)
                self.getRemoteFileList()
            if self.currentFileList == "Local":
                os.remove(deleteFilePath)
                self.LocalFilesList.clear()
                getLocalFileList(self, None, True)
            showDeleteFileSuccessMsg(self)
            return 
        if confirmDelete == QMessageBox.No:
            print("No clicked")
        if confirmDelete == QMessageBox.Cancel:
            print("Cancel")