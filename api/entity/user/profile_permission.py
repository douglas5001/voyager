class Profile:
    def __init__(self, name, permission_ids=None):
        self.__name = name
        self.__permission_ids = permission_ids or []

    @property
    def name(self):
        return self.__name

    @property
    def permission_ids(self):
        return self.__permission_ids

class Permission():
    def __init__(self, name):
        self.__name = name
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        

