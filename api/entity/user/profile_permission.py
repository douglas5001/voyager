class Profile():
    def __init__(self, name):
        self.__name = name
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

class Permission():
    def __init__(self, name):
        self.__name = name
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        

