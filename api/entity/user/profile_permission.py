class Profile():
    def __init__(self, name, permission):
        self.__name = name
        self.permission = permission
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
    
    @property
    def permission(self):
        return self.__permission

    @permission.setter
    def permission(self, permission):
        self.__permission = permission

class Permission():
    def __init__(self, name):
        self.__name = name
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        

