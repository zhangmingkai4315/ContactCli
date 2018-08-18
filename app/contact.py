import os
import json
import app.config as Config
from app.user import User
from app.exception import *
import re

class ContactManager(object):
    def __init__(self, db_file=Config.DEFAULT_DB_FILE):
        self.db_file = db_file

    def __enter__(self):
        try:
            if not os.path.isfile(self.db_file):
                self.contacts = {
                    "version": Config.DB_VERSION,
                    "data": []
                }
            else:
                db_handler = file(self.db_file, "r")
                self.contacts = json.load(db_handler)
                db_handler.close()
        except Exception as e:
            raise ConfigFileParseException(e.message)
        return self
    def __exit__(self,exc_type, exc_val, exc_tb):
        db_handler = file(self.db_file,"w")
        json.dump(self.contacts,db_handler)
        db_handler.close()

    def version(self):
        return self.contacts['version']

    def size(self):
        return len(self.contacts["data"])

    def list_contacts(self):
        return self.contacts["data"]

    def search_contact(self,name):
        matches = []
        for contact in self.contacts["data"]:
            if contact["username"].lower() == (name.lower()):
                matches.append(contact)
        return matches

    def new_contact(self,user):
        if not isinstance(user, User):
            raise UserNotValidException()
        user.index = len(self.contacts["data"])
        self.contacts["data"].append(user.to_object())
        return self
    
    def delete_user(self,index=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        self.contacts["data"].pop(index)
        return self
    
    def update_contact(self,index=None,user=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        if User == None or not isinstance(user,User):
            raise UserNotValidException()
        self.contacts["data"][index] = user.to_object()
        return self
    
    def append_new_phone_with_user_index(self, index=None,phone=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        if not User.valid_phone(phone):
            raise PhoneNotValidException()
        print( self.contacts["data"][index] )
        if phone not in self.contacts["data"][index]["phones"]:
            self.contacts["data"][index]["phones"].append(phone)
        return self

    def delete_phone_with_user_index(self, index=None,phone=None):
        if index == None:
            raise IndexNotGivenException()
        if index<0 or index>=len(self.contacts["data"]):
            raise IndexOutofRangeException()
        if phone in self.contacts["data"][index]["phones"]:
            self.contacts["data"][index]["phones"].remove(phone)
        return self

    
        




            