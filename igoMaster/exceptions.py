#coding:utf-8

class IgoguideBaseException():

    def __init__(self, message):
        self.message = message

    def format(self):
        raise NotImplementedError

####    OBJECT NOT FOUND
class ObjectNotFoundException(IgoguideBaseException):

    def __init__(self,obj,id):
        self.msg=f'{obj} Object by id "{id}" not found!'

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':1
            }
        }

####    OBJECT ALREADY EXISTS
class ObjectAlreadyExistsException(IgoguideBaseException):
    def __init__(self,obj,attr):
        self.msg=f"{obj} Object with the same {attr} attribute already exists"

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':2
            }
        }

####    INVALID REQUEST METHOD
class InvalidRequestMethodException(IgoguideBaseException):

    def __init__(self,wrong_method,right_method):
        self.msg=f"Invalid request method: {wrong_method.upper()} must be {right_method.upper()}!"

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':3
            }
        }

class UncompatibleUserTypeException(IgoguideBaseException):

    def __init__(self,wrong_user_type,right_user_type):
        self.msg=f'Only a {right_user_type} USER can request this action. Not a {wrong_user_type} USER!'

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':4
            }
        }

class UnknownErrorException(IgoguideBaseException):

    def __init__(self,msg):
        self.msg=msg

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':6
            }
        }

class InvalidAuthInformationException(IgoguideBaseException):

    def __init__(self,attribute):
        self.msg="Invalid {attribute} "

    def format(self):
        return {
            'Status':'failed',
            'Error':{
                'name':self.__class__.__name__,
                'message':self.msg,
                'code':7
            }
        }