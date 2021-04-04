import os
import win32api
import time
from datetime import datetime 


file_path1 = "C:\\Users\\sheha\\OneDrive\\Documents\\homeGymApproxCost.txt"
info = os.stat(file_path1)
print(info)
# print(info)
# file_mode = win32api._getFileMode(file_path1)
# files_number = pywin32._getFilesNumber(file_path1)
# group = pywin32._getGroup(file_path1)
modified_time = datetime.fromtimestamp(os.path.getmtime(file_path1)).strftime("%Y-%m-%d %H:%M:%S")
file_size = os.path.getsize(file_path1)
# size = win32api.GetPwrCapabilities(file_path1)
# user = pywin32._getUser(file_path1)
# print("file mode: " + file_mode +
#         "\nfiles number: " + files_number +
#         "\ngroup: " + group + 
#         "\nlast time: " + last_time +
print("Modified time: " + str(modified_time) + "\n" 
        + "size: " + str(file_size) )

        # "\nuser: " + user)
