from PyQt5.QtWidgets import (QMessageBox, QApplication)
import os, paramiko
from local_transfer import getLocalFileList
import logging 
from PyQt5.QtCore import Qt

logger = logging.getLogger('Delete file')
def remoteDelete(self, deleteFilePath):
    errorMessage = QMessageBox()
    errorMessage.setIcon(QMessageBox.Critical)
    errorMessage.setWindowTitle("Deletion Error")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.hostname, username=self.username, password=self.password)
        stdin, stdout, stderr = client.exec_command('rm ' + deleteFilePath)
        client.close()
        return True 
    except paramiko.ssh_exception.SSHException as e:
        QApplication.restoreOverrideCursor()
        errorMessage.setInformativeText(str(e))
        logger.error(e)
        errorMessage.exec_()
        return False 
    except UnicodeDecodeError as e: 
        QApplication.restoreOverrideCursor()
        errorMessage.setInformativeText(str(e))
        logger.error(e)
        errorMessage.exec_()
        return False 
    
def showDeleteFileSuccessMsg(self):
    deleteFile_success_msg = QMessageBox()
    deleteFile_success_msg.setWindowTitle("File deleted")
    deleteFile_success_msg.setText("File deleted successfully!")
    deleteFile_success_msg.setIcon(QMessageBox.Information)
    deleteFile_success_msg.exec_()

def deleteFile(self):
    
    if self.currentFile != "/":
        deleteFile = self.currentFile
        try:
            deleteFileName = str(self.currentFile.text(0))
            deleteFilePath = ""
            if self.currentFileList == "Local": 
                deleteFilePath = self.currentLocalPath + "\\" + deleteFileName
            elif self.currentFileList == "Remote":
                deleteFilePath = self.currentRemotePath + "/" + deleteFileName 
        except AttributeError as e:
            errorMessage = QMessageBox(QMessageBox.Critical, "File not selected", "No file selected to delete! Make sure to select a file first")
            errorMessage.exec_()
            return 
        confirmDelete = QMessageBox.question(self, "Confirm Action", "Are you sure you want to delete this file: " + deleteFilePath, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if confirmDelete == QMessageBox.Yes:
            self.notificationLabel.setText("Loading...")
            QApplication.setOverrideCursor(Qt.WaitCursor)
            if deleteFile.statusTip(0) == "d":
                QApplication.restoreOverrideCursor()
                errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Cannot delete folders! Only files can be deleted...")
                errorMessage.exec_()
                self.notificationLabel.setText("")
                return 
            if self.currentFileList == "Remote":
                if remoteDelete(self, deleteFilePath) == True:
                    QApplication.restoreOverrideCursor()
                    self.getRemoteFileList()
                    showDeleteFileSuccessMsg(self)
            if self.currentFileList == "Local":
                os.remove(deleteFilePath)
                self.LocalFilesList.clear()
                getLocalFileList(self, None, True)
                QApplication.restoreOverrideCursor()
                showDeleteFileSuccessMsg(self)
            self.notificationLabel.setText("")
            return 
        if confirmDelete == QMessageBox.No:
            print("No clicked")
        if confirmDelete == QMessageBox.Cancel:
            print("Cancel")
        QApplication.restoreOverrideCursor()
    self.notificationLabel.setText("")