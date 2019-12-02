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