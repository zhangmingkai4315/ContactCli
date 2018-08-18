import os
import json
import app.config as Config
from app.user import UserNotValidException,User
import re

class ConfigFileParseException(Exception):
    pass
class DuplicateUserException(Exception):
    pass
class IndexOutofRangeException(Exception):
    pass
class IndexNotGivenException(Exception):
    pass

class ContactManager(object):
    def __init__(self, db_file=Config.DEFAULT_DB_FILE):
        try:
            self.db_handler = self.get_file_handler(db_file)
            self.contacts = json.load(self.db_handler)
            self.status = Config.READ_DB_FILE_SUCCESS
        except Exception as e:
            raise ConfigFileParseException(e.message)

    def get_file_handler(self, db_file):
        if not os.path.isfile(db_file):
            db_handler = file(db_file, "w+")
            init_data = {
                "version": Config.DB_VERSION,
                "data": []
            }
            db_handler.write(json.dumps(init_data))
            db_handler.seek(0)
        else:
            db_handler = file(db_file, "r+")
        return db_handler

    def version(self):
        return self.contacts['version']

    def list_contacts(self):
        return self.contacts["data"]

    def search_contact(self,name):
        matches = []
        for contact in self.contacts["data"]:
            if contact["username"].lower() == (name.lower()):
                matches.append(contact)
        return matches

    def insert_contact(self,user):
        if not isinstance(user, User):
            raise UserNotValidException()
        matchers = self.search_contact(user.username)
        if len(matchers) == 0:
            user.index = len(self.contacts["data"])
            self.contacts["data"].append(user.to_object())
        else:
            raise DuplicateUserException()
    
    def delete_user(self,index=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        return self.contacts["data"].pop(index)
    
    def update_contact(self,index=None,user=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        if User == None or not isinstance(user,User):
            raise UserNotValidException()
        self.contacts["data"][index] = user.to_object()

    def close(self):
        json.dump(self.contacts,self.db_handler)
        self.db_handler.close()
    
        




            