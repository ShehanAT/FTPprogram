from PyQt5.QtWidgets import (QMessageBox)
import os 


def showDeleteFileSuccessMsg(self):
    deleteFile_success_msg = QMessageBox()
    deleteFile_success_msg.setWindowTitle("File deleted")
    deleteFile_success_msg.setText("File deleted successfully!")
    deleteFile_success_msg.setIcon(QMessageBox.Information)
    deleteFile_success_msg.exec_()

def deleteFile(self):
    if self.currentFile != "/":
        deleteFile = self.currentFile
        if self.currentFileList == "Remote":
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Cannot delete files and folder in remote server!")
            errorMessage.exec_()
            return 
        if deleteFile.background().color().getRgb() == (100, 100, 150, 255):
            errorMessage = QMessageBox(QMessageBox.Critical, "Error", "Cannot delete folders! Only files can be deleted...")
            errorMessage.exec_()
            return 
        deleteFileName = str(self.currentFile.text())
        deleteFilePath = deleteFileName.split(" -")[0]
        
        confirmDelete = QMessageBox.question(self, "Confirm Action", "Are you sure you want to delete this file: " + deleteFilePath, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if confirmDelete == QMessageBox.Yes:
            os.remove(deleteFilePath)
            showDeleteFileSuccessMsg(self)
            self.LocalFilesList.clear()
            self.getLocalFileList(None, True)
        if confirmDelete == QMessageBox.No:
            print("No clicked")
        if confirmDelete == QMessageBox.Cancel:
            print("Cancel")