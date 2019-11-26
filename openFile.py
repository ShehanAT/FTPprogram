#!/usr/bin/env 

fh = None 
try: 
    try: 
        fh = open("./textFile.txt")
        print(fh.read())
    except IOError as e:
        print("I/O error: %s" % e)
finally:
    if fh:
        fh.close()