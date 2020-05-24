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

    # User Test
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
       
    # Playlist Test
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
        self.assertTrue(getPlaylist(playlist1.id))
        deletePlaylist(playlist1.id)
        self.assertFalse(getPlaylist(playlist1.id))

    def test_getPlaylistName(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        playlist2 = createNewPlaylist('Arcade Fire')
        self.assertEqual(getPlaylistName(playlist1.id),'Juice Wrld')
        self.assertEqual(getPlaylistName(playlist2.id),'Arcade Fire')

    # Songs Test
    def test_addSongInPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        self.assertFalse(len(getSongsInPlaylist(playlist1.id))>0)
        addSongInPlaylist(song1.id, playlist1.id)
        self.assertTrue(len(getSongsInPlaylist(playlist1.id))>0)

    def test_deleteSongInPlaylist(self):
        playlist1 = createNewPlaylist('Juice Wrld')
        song1 = addSongDetails('1', '#', '#', 'Robbery', 'Juice Wrld', 'Death Race for Love')
        addSongInPlaylist(song1.id, playlist1.id)
        self.assertTrue(len(getSongsInPlaylist(playlist1.id))>0)
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
        self.assertEqual(song2, all[1])

    # Results Test
    def test_addIndividualResults(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        playlist1 = createNewPlaylist("Some Hits")
        song1 = addSongDetails("someId", "someURL", "someIMG", "someName", "someArtist", "someAlbum")
        addSongInPlaylist(song1.id, playlist1.id)

        self.assertFalse(len(Results.query.all())==1)
        self.assertFalse(len(IndividualResults.query.all())==2)

        addIndividualResults(user1.id, playlist1.id, "wrongAnswer", "wrongAnswer", song1.id, False, False)
        addIndividualResults(user1.id, playlist1.id, "someName", "someArtist", song1.id,True, True)

        self.assertTrue(len(Results.query.all())==1)
        self.assertTrue(len(IndividualResults.query.all())==2)

    def test_getResultsOfUser(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        playlist1 = createNewPlaylist("Some Hits")
        playlist2 = createNewPlaylist("Another Playlist")

        song1 = addSongDetails("someId","someURL","someIMG","someName","someArtist","someAlbum")
        song2 = addSongDetails("someId2","someURL2","someIMG2","someName2","someArtist2","someAlbum2")

        # 2 different playlist played by User
        addSongInPlaylist(song1.id, playlist1.id)
        addSongInPlaylist(song2.id, playlist2.id)

        individualResult1=addIndividualResults(user1.id, playlist1.id, song1.id, "wrongAnswer", "wrongAnswer", False, False)
        individualResult2=addIndividualResults(user1.id, playlist2.id, song2.id, "someName", "someArtist", True, True)

        compiledResultDict = getResultsOfUser(1)

        playlistResult1 = compiledResultDict[0]
        playlistResult2 = compiledResultDict[1]

        self.assertTrue(playlistResult1["playlistId"],1)
        self.assertTrue(playlistResult2["playlistId"], 2)

        self.assertTrue(playlistResult1["userId"],1)
        self.assertTrue(playlistResult2["userId"], 1)

        individualResult1= playlistResult1["results"][0]
        individualResult2 = playlistResult2["results"][0]

        self.assertTrue(individualResult1["answerArtist"],"wrongAnswer")
        self.assertTrue(individualResult2["answerArtist"], "someName")

    def test_deleteResults(self):
        user1 = createNewUser("Frinze", "CorrectPassword", "Email@gmail.com")
        playlist1 = createNewPlaylist("Some Hits")
        song1 = addSongDetails("someId", "someURL", "someIMG", "someName", "someArtist", "someAlbum")
        addSongInPlaylist(song1.id, playlist1.id)

        addIndividualResults(user1.id, playlist1.id, "wrongAnswer", "wrongAnswer", song1.id, False, False)
        addIndividualResults(user1.id, playlist1.id, "someName", "someArtist", song1.id,True, True)

        self.assertTrue(len(Results.query.all())==1)
        self.assertTrue(len(IndividualResults.query.all()) == 2)

        deleteResults(1)

        self.assertTrue(len(Results.query.all())==0)
        self.assertTrue(len(IndividualResults.query.all()) == 0)






if __name__ == "__main__":
    unittest.main()