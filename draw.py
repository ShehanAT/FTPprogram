from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, 
    QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, 
    QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QToolButton, QMessageBox, QFrame, QFileDialog, QMainWindow, QGraphicsColorizeEffect, QMessageBox)
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import os 

def createTopTextBoxes(self):
    self.hostnameTextBox = QLineEdit(self)
    self.hostnameTextBox.move(200, 70)
    self.hostnameTextBox.resize(280, 40)
    self.hostnameTextBox.setPlaceholderText("Hostname: ")

    self.usernameTextBox = QLineEdit(self)
    self.usernameTextBox.move(550, 70)
    self.usernameTextBox.resize(280, 40)
    self.usernameTextBox.setPlaceholderText("Username: ")

    self.passwordTextBox = QLineEdit(self)
    self.passwordTextBox.setEchoMode(QLineEdit.Password)
    self.passwordTextBox.move(875, 70)
    self.passwordTextBox.resize(280, 40)
    self.passwordTextBox.setPlaceholderText("Password: ")

    self.quickConnectButton = QPushButton(self)
    self.quickConnectButton.setDefault(True)
    self.quickConnectButton.move(1300, 70)
    self.quickConnectButton.resize(150, 40)
    self.quickConnectButton.setText("Quick Connect")
    self.quickConnectButton.setStyleSheet('QPushButton {background-color: #fff; color: black; border: 1px solid blue;}')
    self.hostname = self.hostnameTextBox.text()
    self.username = self.usernameTextBox.text()
    self.password = self.passwordTextBox.text()
    # self.quickConnectButton.clicked.connect(startFTP(self, self.hostnameTextBox.text(), self.usernameTextBox.text(), self.passwordTextBox.text()))
    self.show()

def createBottomCenterBox(self):
    self.rightArrowButton = QToolButton(self)
    self.rightArrowButton.setIcon(QIcon(os.getcwd() + "/icons/right.png" ))
    self.rightArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
    self.rightArrowButton.setCursor(Qt.ArrowCursor)
    self.rightArrowButton.resize(45, 45)
    self.rightArrowButton.move(710, 250)
    # self.rightArrowButton.clicked.connect(lambda:self.remoteToLocalTransfer(self.remoteSelectedFile))
    self.rightArrowButton.setEnabled(False)

    self.leftArrowButton = QToolButton(self)
    self.leftArrowButton.setIcon(QIcon(os.getcwd() + "/icons/left.png"))
    self.leftArrowButton.setStyleSheet("border: 1px solid black; padding: 1px; background-color: #6BA4FC")
    self.leftArrowButton.setCursor(Qt.ArrowCursor)
    self.leftArrowButton.resize(45, 45)
    self.leftArrowButton.move(710, 315)
    # self.leftArrowButton.clicked.connect(lambda:self.localToRemoteTransfer(self.localSelectedFile))
    self.leftArrowButton.setEnabled(False)

def createDeleteButton(self):
    self.deleteButton = QPushButton(self)
    self.deleteButton.setIcon(QIcon(os.getcwd() + "/icons/delete.png"))
    self.deleteButton.setCursor(Qt.ArrowCursor)
    self.deleteButton.resize(35, 35)
    self.deleteButton.move(20, 70)
    
    self.deleteButton.setEnabled(True)
    self.deleteButton.show()

def createBottomRightBox(self):        
    self.LocalFilesList.move(800, 160)
    self.LocalFilesList.resize(650, 570)
    self.LocalFilesList.setColumnCount(3)
    self.LocalFilesList.setHeaderLabels(["Name", "Date Modified", "Size"])


    self.LocalFilesLabel = QLabel(self)
    self.LocalFilesLabel.setText("Local Files Section:\n{file} - {size}") 
    self.LocalFilesLabel.move(800, 120)
    self.LocalFilesLabel.adjustSize()
    self.LocalFilesList.itemDoubleClicked.connect(self.localFileSelectionChanged)
    self.LocalFilesList.itemClicked.connect(self.localFileSelectionChangedSingleClick)

def createBottomLeftBox(self):
    self.RemoteFilesList.move(20, 160)
    self.RemoteFilesList.resize(650, 570)
    self.RemoteFilesList.setColumnCount(3)
    self.RemoteFilesList.setHeaderLabels(["Name", "Date Modified", "Size"])
    self.remoteSelectedFile = [] 

    self.RemoteFilesLabel = QLabel(self)
    self.RemoteFilesLabel.setText("Remote Files Section:\n{file} - {size}")
    self.RemoteFilesLabel.move(20, 120)
    self.RemoteFilesLabel.adjustSize()
    self.RemoteFilesList.itemDoubleClicked.connect(self.remoteFileSelectionChanged)
    self.RemoteFilesList.itemClicked.connect(self.remoteFileSelectionChangedSingleClick)

def createNotificationBox(self):
    self.notificationLabel = QLabel(self)
    self.notificationLabel.setText("Please enter remote credentials to continue...")
    self.notificationLabel.setAlignment(Qt.AlignTop)
    self.notificationLabel.resize(400, 20)
    self.notificationLabel.setGeometry(500, 25, 600, 100)
    self.notificationLabel.setFont(QFont('Times', 12))
    red_font = QGraphicsColorizeEffect()
    red_font.setColor(QColor(255, 15, 15))
    self.notificationLabel.setGraphicsEffect(red_font)
