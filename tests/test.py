import unittest, os

import sys
sys.path.append(".")
from app import app, db
from app.models import *
from app.controllers import *

class UserControllerCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()  # Creates virtual test environment
        db.create_all()

        # Setting Up Some Data If Needed

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_createNewUser(self):
        user1 = createNewUser("Frinze", "Password", "Email@gmail.com")
        user2 = createNewUser("Sarup", "SomePass", "Email2@gmail.com")

        all = User.query.all()
        self.assertEqual(user1,all[0])
        self.assertEqual(user2, all[1])

    def test_createNewAdmin(self):
        admin1 = createNewAdmin("Frinze", "Password", "Email@gmail.com")
        user1 = createNewUser("Sarup", "SomePass", "Email2@gmail.com")
        all = User.query.all()

        self.assertTrue(admin1.is_admin())
        self.assertFalse(user1.is_admin())

    def test_validateUserLogin(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        self.assertTrue(validateUserLogin("Frinze","CorrectPassword"))
        self.assertFalse(validateUserLogin("Frinze", "Wrong Password"))

    def test_isUsernameTaken(self):
        user1 = createNewUser("Frinze", "Password", "Email@gmail.com")
        self.assertTrue(isUsernameTaken("Frinze"))
        self.assertFalse(isUsernameTaken("Sarup"))

    def test_isEmailTaken(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        self.assertTrue(isEmailTaken("Email@gmail.com"))
        self.assertFalse(isEmailTaken("abc@gmail.com"))
   
    def test_deleteUser(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        all = len(User.query.all())
        self.assertEqual(1, all)
        deleteUser(user1.username)
        all = len(User.query.all())
        self.assertEqual(0, all)

    def test_doesThisMatch(self):
        self.assertTrue(doesThisMatch("Taylor Swift", "Tayla Swift"))
        self.assertFalse(doesThisMatch("Taylor", "Hello"))
       
if __name__ == "__main__":
    unittest.main()