import re
from app.exception import UserNotValidException

class User(object):
    def __init__(self,username=None,phones=None,index=None):
      self.username = username
      self.phones = phones if type(phones) is list else [phones]
      self.index = index if index is not None else -1
      if not self.validate_user():
        raise UserNotValidException()

    @staticmethod
    def valid_phone(phone):
      if not isinstance(phone,basestring):
        return False
      if phone is None or not re.match(r"1\d{10}",phone):
        return False      
      return True

    def validate_user(self):
      if self.username == None:
        return False  
      if not isinstance(self.username,basestring) or len(self.username)==0:
        return False
      if not isinstance(self.index,int):
        return False
      for phone in self.phones:
        isValidPhone = self.valid_phone(phone)
        if isValidPhone == False:
          return False
      return True

    def to_object(self):
      return {
        "index":self.index,
        "username":self.username,
        "phones":self.phones
      }
    def __repr__(self):
      return "<Username:{0},Phone:{1}>".format(self.username,",".join(self.phones))