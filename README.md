# FTP Program Overview
This is a FTP Client program built using Python and the PyQt5 GUI framework. It allows users to connect to remote servers, browse their remote & local file systems, transfer files from remote to local & local to remote, and delete files on both remote and local file systems.

It also includes a SFTP server that the user can run locally.

# Purpose:
I built this application primarily in order to gain experience making small projects using Python and to mentor new Python developers on Python software development. 

### Dependencies:
* Python 3.9.x
* PyQt5.x
* pysftp 0.2.9
* pathlib
* sftpserver

### Platform:
This program was developed on Windows but can also run on Unix like operating systems such as Linux and Mac OSX. 

# Local deployment instructions: 
1. Clone repo
2. open project folder in IDE of your choice  
3. run ```python main.py```

# Application Usage instructions:
1. Enter your hostname, username, and password in the corresponding field at the top, where hostname is the server ip address of your remote server(it can be a DigitalOcean droplet)
2. Click the ```Quick Connect``` button 
3. Single click a directory to traverse the local & remote file systems
4. Double click to select file, then press corresponding arrow button to transfer from local to remote or visa versa 
5. Double click and press Trash icon button to delete selected file

# Screenshots: 
FTP Client starting screen after FTP login: 
![FTP Client starting screen after FTP login](https://github.com/ShehanAT/FTPprogram/blob/master/screenshots/client_starting_screen.png)

FTP Client Remote to Local file transfer success:
![FTP Client file transfer success](https://github.com/ShehanAT/FTPprogram/blob/master/screenshots/remote_to_local_transfer.png)

FTP Client file deletion success:
![FTP Client file delete](https://github.com/ShehanAT/FTPprogram/blob/master/screenshots/delete_success.png)

FTP Client exception thrown:
![FTP Client exception thrown](https://github.com/ShehanAT/FTPprogram/blob/master/screenshots/exception_thrown.png)

### Contributing:
Please feel free to contribute to this project however possible by forking this repo, making changes and initiating pull requests. Thanks!
