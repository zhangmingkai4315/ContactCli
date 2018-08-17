import unittest
import os
from app.contact import ContactManager, ConfigFileParseException
import app.config as Config


class TestContactManager(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(Config.DEFAULT_DB_FILE):
            os.remove(Config.DEFAULT_DB_FILE)

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


if __name__ == '__main__':
    unittest.main()
