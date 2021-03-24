import re 
import os
currentLocalPath = 'C:\\Users\shehan\OneDrive\Documents\Github'
currentLocalPath2 = 'C:\\Users\\shehan\\OneDrive\\Documents\\Github'
# newLocalArr = currentLocalPath.split("/")
newLocalArr = os.path.split(currentLocalPath)
newLocalArr2 = os.path.split(currentLocalPath2)
newPath = list(newLocalArr)[0]
newPath2 = list(newLocalArr2)[0]
print("passing")