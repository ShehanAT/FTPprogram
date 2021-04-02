from pysftp import paramiko
import pysftp, os, logging
import os
from base64 import decodebytes 

hostname='167.99.187.80'
user = 'root'
password = 'Shehan123'
private_key = "C:\\Users\\sheha\\Downloads\\id_rsa"
port = 22 

# keydata = b"""AAAAB3NzaC1yc2EAAAADAQABAAABgQDIuVReRAZ0mae8yPGfZ7axY+oPeyFS418Io2rG/yYn//yK1WtFkKI49x7HStX/hu/V24cRUWVgfi5iJsuCyHXLvpZPBTW6T1z7DaG5O9s9rekfW3aQEO2KcZlRD33n57qntkDOH1Ps6nBE83a4DwgZ1xdim2s2nTdOsefc+Xdg0jp639QV9xnSp9UWuPc3hvj583uirukDlftaszLQ8aTW932i59Y7ELt45vriKzgjvXXyWeL1Wg+MX8nsffBtXLIrCVqAJCtWDRf/Jytm0PABSGfuiZyMCTbiep3aysL98S5+6Z2cKObAYdOO2RqssWmJT24H8E8hh430wr4TRBCwW62OI8CaB+cHDWv+VWiRzQXfeuNXBYaSZh9pqCOfdEOrHWfLniSz7JYAX0LsMsWbtVt5MgUYnQZ6xBtwb0qq2BJSGePgNfFSQ+hwcciBFT/65GTIxO/+7Drf6Eexn7wMsxYSMd+dXbHfqv7zMBkzFICzwkkA/15U6syK3fmV6Us="""
key = paramiko.RSAKey(filename="C:\\Users\\sheha\\Downloads\\id_rsa")
# Open a transport
ssh = paramiko.SSHClient()
ssh.get_host_keys().add('167.99.187.80', 'ssh-rsa', key)
# Auth 
username = "root"
ssh.connect(hostname, username=user, pkey=key)

# Go! 
sftp = ssh.open_sftp()
# sftp://127.0.0.1/FTPTest.txt
sftp.get("./desktop.ini", "C:\\Users\\sheha\\OneDrive\\Documents\\Github\\desktop.ini")

# Close
# if sftp:
#     sftp.close()

'''
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
logger = logging.getLogger()
ssh.connect(hostname, username=username, password=password, key_filename=private_key)
try:
    stdin, stdout, stderr = ssh.exec_command("pwd")
    print(stdout.read())
    print("Passing")
except paramiko.ssh_exception.SSHException as e:
    logger.error(e)

# print(stdout.readlines())
# print("Error: \n")
# print(stderr)
ssh.close()
'''