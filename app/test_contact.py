import unittest
import os
from app.contact import *
import app.config as Config


class TestContactManager(unittest.TestCase):
    def setUp(self):
        pass

    # def tearDown(self):
    #     if os.path.isfile(Config.DEFAULT_DB_FILE):
    #         os.remove(Config.DEFAULT_DB_FILE)

    def test_init_db_file_with_filename(self):
        _ = ContactManager(db_file="test.db")
        isDBFileExist = os.path.isfile("test.db")
        self.assertTrue(isDBFileExist)
        os.remove("test.db")

    def test_init_db_file_with_default(self):
        _ = ContactManager()
        isDBFileExist = os.path.isfile(Config.DEFAULT_DB_FILE)
        self.assertTrue(isDBFileExist)

    def test_read_db_file_with_right_format(self):
        cm = ContactManager(db_file="./test_data/contact.db")
        self.assertEqual(cm.status, Config.READ_DB_FILE_SUCCESS)

    def test_read_db_file_with_fail_format(self):
        with self.assertRaises(ConfigFileParseException):
            _ = ContactManager(db_file="./test_data/failed_contact.db")

    def test_read_init_db_file_return_empty_list(self):
        cm = ContactManager()
        contacts = cm.list_contacts()
        self.assertEquals(contacts, [])

    def test_read_init_db_file_return_correct_version(self):
        cm = ContactManager()
        version = cm.version()
        self.assertEqual(version, Config.DB_VERSION)

    def test_insert_contact_with_wrong_correct(self):
        cm = ContactManager()
        user = "mike"
        with self.assertRaises(UserNotValidException):
            cm.insert_contact(user)

    def test_insert_contact_with_user_object(self):
        cm = ContactManager()
        user = User("Mike", "13800000000")
        cm.insert_contact(user)
        self.assertEqual(len(cm.contacts["data"]), 1)
        self.assertDictEqual(cm.contacts["data"][0], {
            "index": 0,
            "username": user.username,
            "phone": user.phones
        })

    def test_search_contact_with_user_name(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        user1 = User("Alice", "13100000000")
        cm.insert_contact(user0)
        cm.insert_contact(user1)
        matches = cm.search_contact(user0.username)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["username"], user0.username)

        matches = cm.search_contact("MIKE")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["username"].lower(), "MIKE".lower())

        with self.assertRaises(DuplicateUserException):
            cm.insert_contact(user0)

    def test_search_contact_with_not_exist_user(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        matches = cm.search_contact("alice")
        self.assertEqual(len(matches), 0)

    def test_delete_user_with_index(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        matches = cm.search_contact("Mike")  
        self.assertEqual(len(matches), 1) 
        matches = cm.delete_user(0)
        matches = cm.search_contact("Mike")     
        self.assertEqual(len(matches), 0)

    def test_delete_user_with_out_of_index(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        matches = cm.search_contact("Mike")  
        self.assertEqual(len(matches), 1) 
        with self.assertRaises(IndexOutofRangeException):
            matches = cm.delete_user(10)

    def test_delete_user_with_no_index(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        with self.assertRaises(IndexNotGivenException):
            _ = cm.delete_user()

    def test_update_user_with_no_index(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        with self.assertRaises(IndexNotGivenException):
            _ = cm.update_contact()

    def test_update_user_with_no_user(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        with self.assertRaises(UserNotValidException):
            _ = cm.update_contact(index=0)
    
    def test_update_user_with_no_correct_user_type(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)
        with self.assertRaises(UserNotValidException):
            _ = cm.update_contact(index=0,user="test")

    def test_save_contact(self):
        cm = ContactManager()
        user0 = User("Mike", "13800000000")
        cm.insert_contact(user0)       
        cm.close()
        other_cm = ContactManager()
        matches = other_cm.search_contact("mike")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["username"], "mike")

if __name__ == '__main__':
    unittest.main()
