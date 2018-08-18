import unittest
from app.user import User
from app.exception import UserNotValidException

class TestUserClass(unittest.TestCase):
  def test_init_user_with_correct_info(self):
    username = "mike"
    phones = "13800000000"
    user = User(username,phones)
    self.assertEqual(user.username, username)
    self.assertEqual(user.phones,[phones])
    self.assertEqual("<Username:{0},Phone:{1}>".format(username,phones),str(user))
  
  def test_init_user_with_not_correct_info(self):
    users = [
      {"username":"","phones":"13800000000"},
      {"username":"","phones":"138"},
      {"username":None,"phones":None},
      {"username":"mike","phones":None},
      {"username":12,"phones":"13800000000"}
    ]
    for user in users:
      with self.assertRaises(UserNotValidException):
        _ = User(user["username"],user["phones"])

    with self.assertRaises(UserNotValidException):
      _ = User("Mike")
    with self.assertRaises(UserNotValidException):
      _ = User(phones="13800000000")
    with self.assertRaises(UserNotValidException):
      _ = User(username="Mike",phones="13800000000",index="not_int_type")    
    
  def test_user_to_object(self):
    username = "mike"
    phones = "13800000000"
    user = User(username,phones)
    user_object = user.to_object()
    self.assertDictEqual(user_object,{
      "index":-1,
      "username":user.username,
      "phones":user.phones
    })
  def test_valid_phone(self):
    phones = [
      ["13800000000",True],
      ["138000000002",False],
      ["138",False],
      ["Hello",False],
      ["1234None",False],
      [None,False],
      [123,False],
      [13800000000,False]]
    for phone in phones:
      self.assertEqual(User.valid_phone(phone[0]),phone[1])
