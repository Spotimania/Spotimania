import unittest, os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    def test_createNewPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        self.assertTrue(getPlaylist(playlist1.id))
        self.assertFalse(getPlaylist(playlist1.id) is None)

    def test_editPlaylistName(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        editPlaylist1 = editPlaylistName(playlist1.id, 'Arcade Fire')
        self.assertTrue(getPlaylistName(playlist1.id) == 'Arcade Fire')
        self.assertFalse(getPlaylistName(playlist1.id) == 'Juice Wrld')

    def test_deletePlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        deletePlaylist(playlist1.id)
        self.assertTrue(getPlaylist(playlist1.id) is None)
        self.assertFalse(getPlaylist(playlist1.id))

    def test_getPlaylistName(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        playlist2 = createNewPlaylist('Arcade Fire')
        self.assertEqual(getPlaylistName(playlist1.id),'Juice Wrld')
        self.assertEqual(getPlaylistName(playlist2.id),'Arcade Fire')

    def test_addSongInPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        addSongInPlaylist(song1.id, playlist1.id)
        self.assertTrue(len(getSongsInPlaylist(playlist1.id))>0)

    def test_deleteSongInPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        addSongInPlaylist(song1.id, playlist1.id)
        deleteSongInPlaylist(song1.id, playlist1.id)
        self.assertFalse(len(getSongsInPlaylist(playlist1.id))>0)

    def test_getSongsInPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        song2 = addSongDetails('2', '#', '#', 'Hurt Me', 'Juice Wrld', 'Goodbye & Good Riddance')
        addSongInPlaylist(song1.id, playlist1.id)
        addSongInPlaylist(song2.id, playlist1.id)
        self.assertTrue(len(getSongsInPlaylist(playlist1.id))==2)
        self.assertEqual(getSongsInPlaylist(playlist1.id)[0]['songName'],'Robbery')
        self.assertEqual(getSongsInPlaylist(playlist1.id)[1]['songName'],'Hurt Me')

    def test_getSongDetails(self):
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        song2 = addSongDetails('2', '#', '#', 'Hurt Me', 'Juice Wrld', 'Goodbye & Good Riddance')
        self.assertEqual(getSongDetails(song1.id).album,'Death Race for Love')
        self.assertEqual(getSongDetails(song2.id).songName,'Hurt Me')

    def test_addSongDetails(self):
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        song2 = addSongDetails('2', '#', '#', 'Hurt Me', 'Juice Wrld', 'Goodbye & Good Riddance')
        all = Song.query.all()
        self.assertEqual(song1,all[0])
        self.assertEqual(song2,all[1])


if __name__ == "__main__":
    unittest.main()