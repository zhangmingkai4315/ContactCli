import unittest
import os
from app.contact import ContactManager
import app.config as Config
from app.user import User
from app.exception import *

class TestContactManager(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(Config.DEFAULT_DB_FILE):
            os.remove(Config.DEFAULT_DB_FILE)

    def test_init_db_file_with_filename(self):
        with ContactManager(db_file="test.db") as cm:
            pass
        isDBFileExist = os.path.isfile("test.db")
        self.assertTrue(isDBFileExist)
        os.remove("test.db")

    def test_init_db_file_with_default(self):
        with ContactManager() as cm:
            pass
        isDBFileExist = os.path.isfile(Config.DEFAULT_DB_FILE)
        self.assertTrue(isDBFileExist)

    def test_read_db_file_with_right_format(self):
        with ContactManager(db_file="./test_data/contact.db") as cm:
            pass
        self.assertEqual(cm.db_file,"./test_data/contact.db")

    def test_read_db_file_with_fail_format(self):
        with self.assertRaises(ConfigFileParseException):
            with ContactManager(db_file="./test_data/failed_contact.db") as cm:
                pass

    def test_read_init_db_file_return_empty_list(self):
        with ContactManager() as cm:
            contacts = cm.list_contacts()
            self.assertEquals(contacts, [])

    def test_read_init_db_file_return_correct_version(self):
        with ContactManager() as cm:
            version = cm.version()
            self.assertEqual(version, Config.DB_VERSION)

    def test_read_init_db_file_return_zero_size(self):
        with ContactManager() as cm:
            size = cm.size()
            self.assertEqual(size,0)

    def test_new_contact_with_wrong_correct(self):
        with ContactManager() as cm:
            user = "mike"
            with self.assertRaises(UserNotValidException):
                cm.new_contact(user)

    def test_new_contact_with_user_object(self):
        with ContactManager() as cm:
            user = User("Mike", "13800000000")
            cm.new_contact(user)
            self.assertEqual(len(cm.contacts["data"]), 1)
            self.assertDictEqual(cm.contacts["data"][0], {
                "index": 0,
                "username": user.username,
                "phones": user.phones
            })

    def test_search_contact_with_user_name(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            user1 = User("Alice", "13100000000")
            cm.new_contact(user0)
            cm.new_contact(user1)
            matches = cm.search_contact(user0.username)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["username"], user0.username)
            matches = cm.search_contact("MIKE")
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["username"].lower(), "MIKE".lower())

    def test_search_contact_with_not_exist_user(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            matches = cm.search_contact("alice")
            self.assertEqual(len(matches), 0)

    def test_delete_user_with_index(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            matches = cm.search_contact("Mike")  
            self.assertEqual(len(matches), 1) 
            matches = cm.delete_user(0)
            matches = cm.search_contact("Mike")     
            self.assertEqual(len(matches), 0)

    def test_delete_user_with_out_of_index(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            matches = cm.search_contact("Mike")  
            self.assertEqual(len(matches), 1) 
            with self.assertRaises(IndexOutofRangeException):
                matches = cm.delete_user(10)

    def test_delete_user_with_no_index(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            with self.assertRaises(IndexNotGivenException):
                _ = cm.delete_user()

    def test_delete_all_contacts(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            user1 = User("Mike", "13800000001")
            cm.new_contact(user0).new_contact(user1)
            self.assertEqual(cm.size(),2)
        with ContactManager() as cm:
            cm.delete_all_contacts()
            self.assertEqual(cm.size(),0)


    def test_update_user_with_no_index(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            with self.assertRaises(IndexNotGivenException):
                _ = cm.update_contact()

    def test_update_user_with_no_user(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            with self.assertRaises(UserNotValidException):
                _ = cm.update_contact(index=0)
    
    def test_update_user_with_no_correct_user_type(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
            with self.assertRaises(UserNotValidException):
                _ = cm.update_contact(index=0,user="test")

    def test_save_contact(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            cm.new_contact(user0)
        with ContactManager() as other_cm:
            matches = other_cm.search_contact("mike")
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["username"].lower(), "mike")


    def test_append_new_phone_with_user_index(self):
        with ContactManager() as cm:
            user0 = User("Mike","13800000000")
            cm.new_contact(user0)
            cm.append_new_phone_with_user_index(0,"13810000000")
            phones = cm.contacts["data"][0]["phones"]
            self.assertEqual(len(phones),2)
            self.assertIn("13800000000",phones)
            self.assertIn("13810000000",phones)
            cm.append_new_phone_with_user_index(0,"13810000000")
            phones = cm.contacts["data"][0]["phones"]
            self.assertEqual(len(phones),2)
            with self.assertRaises(PhoneNotValidException):
                cm.append_new_phone_with_user_index(0,"not valid phone")
            
    def test_delete_new_phone_with_user_index(self):
        with ContactManager() as cm:
            user0 = User("Mike","13800000000")
            cm.new_contact(user0)
            cm.delete_phone_with_user_index(0,"13810000000")
            phones = cm.contacts["data"][0]["phones"]
            self.assertEqual(len(phones),1)
            self.assertIn("13800000000",phones)
            cm.delete_phone_with_user_index(0,"13800000000")
            phones = cm.contacts["data"][0]["phones"]
            self.assertEqual(len(phones),0)
         
        
    def test_many_ops_with_in_single_process(self):
        with ContactManager() as cm:
            user0 = User("Mike", "13800000000")
            user1 = User("Alice", "13810000000")
            user0_update = User("Mike", "13820000000")
            cm.new_contact(user0).new_contact(user1).update_contact(0,user0_update)
            current_contacts = cm.list_contacts()
            self.assertEqual(len(current_contacts),2)
            self.assertEqual(current_contacts[0]["username"],"Mike")
            self.assertEqual(current_contacts[0]["phones"],["13820000000"])
            self.assertEqual(2,cm.size())

        with ContactManager() as cm:
            matches = cm.search_contact("Mike")
            self.assertEqual(len(matches),1)
            self.assertEqual(matches[0]["username"],"Mike")

        with ContactManager() as cm:
            cm.delete_user(0)
            self.assertEqual(1,cm.size())



if __name__ == '__main__':
    unittest.main()
