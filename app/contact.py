import os
import json
import app.config as Config

class ConfigFileParseException(Exception):
  pass

class ContactManager(object):
    def __init__(self,db_file=Config.DEFAULT_DB_FILE):
      try:
        self.db_handler = self.get_file_handler(db_file)
        self.contact = json.load(self.db_handler)
        self.status = Config.READ_DB_FILE_SUCCESS
      except Exception as e:
        raise ConfigFileParseException(e.message)

    def get_file_handler(self,db_file):
      if not os.path.isfile(db_file):
        db_handler = file(db_file,"w+")
        init_data = {
          "version":Config.DB_VERSION,
          "data":[]
        }
        db_handler.write(json.dumps(init_data))
        db_handler.seek(0)
      else:
        db_handler = file(db_file,"r+")
      return db_handler

    def version(self):
      if self.status == Config.READ_DB_FILE_FAIL:
        raise 
      return self.contact['version']
      
    def list(self):
      return self.contact["data"]
    

        
        