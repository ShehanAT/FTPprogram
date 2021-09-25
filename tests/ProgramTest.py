import sys 
import unittest 
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtTest import QTest 
from PyQt5.QtCore import Qt 
from program import Program 

class ProgramTest(unittest.TestCase):
    program = program.Program()

    def setUp(self):
        self.program = program
        self.program.show()
        
    def test_defaults(self):
        self.assertEqual(self.program.currentLocalPath, "\\")
        self.assertEqual(self.program.currentRemotePath, "/")
