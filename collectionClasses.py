import bisect 


class OrderedDict(object):
    def __init__(self, dictionary=None):
        self.__keys = [] # this is a list/array 
        self.__dict = {} # this is a dictionary/hash table 
        if dictionary is not None:
            if isinstance(dictionary, OrderedDict):
                self.__dict = dictionary.__dict.copy() # convert passed dictionary 
                self.__keys = dictionary.__keys[:]
            else:
                self.__dict = dict(dictionary).copy() # convert to dictionary then copy 
                self.__keys = sorted(self.__dict.keys())
            
    def getAt(self, index):
        return self.__dict[self.__keys[index]] # get the value at the passed index, where index is a numerical value 

    def setAt(self, index, newValue):
        self.__dict[self.__keys[index]] = newValue # sets new value at the passed index 