# CITS3403-Project2
### "Spotimania"
Aditya Gupta, Frinze Lapuz, Hadi Navabi, Sarup Parajuli

## Table of Contents
1. [Introduction](#intro)
2. [Assessment Mechanism](#assMech)
3. [App Architecture](#appArch)
4. [App Launch](#appLaunch)
5. [App Testing](#appTest)

<a name="intro"></a>
## Introduction 
"Spotimania" is a web application based on the Flask server side rendering micro-framework.
The inspiration for this app comes from the Spotify API which has been used here to create song quizzes for anyone who registers into the application with a personal acccount. The user is then able to play certain pre-made playlists with multiple people in real-time (through sockets). The quiz itself will require the user to guess the name and the artist for the 30 second demo of the song, and at the end of each question they will receive instant feedback comprising of the correct answers and the scores of all the users that are playing together.

After all the questions have been answered, the user can then click on the results page to see his/her full history of results of every playlist that has been attempted by them. The application also provides administration privileges that allows an admin to add/delete/customise playlists that are available to users. This application provides an excellent and fun quiz for both music lovers and just the casual listener to not only test their knowledge of certain music genres, artists, etc, but also a chance to delve into different music cultures.

<a name="assMech"></a>
## Assessment Mechanism
Spotimania uses 'fuzzy matching' of short answers as its primary assessment mechanism. The python module of 'fuzzywuzzy' has been imported into the flask application which is then used to check if the short answer provided by the user obtains a similarity score of greater than 80/100 based on the fuzzy matching algorithm when compared to the actual answer. We have chosen 80 as our benchmark as when testing the fuzzy algortihm, we found it is quite sensitive in scenarios when even a single letter has been accidentally left out or misspelt compared to the answer and we did not wish to penalise users based on minor spelling errors if it was clear they had identified the correct answer.

 <a name="appArch"></a>
## App Architecture (Flask)
This application has been constructed using the python Flask microframeowork MVC. In terms of the Model View Controller Architecture, in our application, the model is represented by the SQLite database and SQLAlchemy, the View is represented by the server-side rendering template of jinja2 which assembles the HTML static content based on the request and the Controller is represented by the Python Flask library.

<a name="appLaunch"></a>
## Using Spotimania 
As with most Flask applications, launching this application requires running the Flask package using `$ flask run` in the directory of the application which will then result in the application being hosted on a local server, usually: http://127.0.0.1:5000/. However, Spotimania has also been deployed on Heroku, and therefore can be accessed directly from the web via the link: https://spotimania.herokuapp.com/.

 <a name="appTest"></a>
## App Testing
Our application has been contructed with testers for all the essential controllers that are based on the CRUD operations of the models. To run the tests, we can simply type `python tests/test.py` in the directory of the application as all of our test are contained in the test.py file. Some of the controllers that are writen are:
#### getResultsOfUser(userId):
This controller collates all the individual results (attempts of song/artist guesses) for all the playlists played by the user.
#### test_getResultsOfUser()

``` python
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
```
This test simulates one user that has played 2 playlists where each playlist contains only one song. The test checks the correctness of the retrieval of the data.
#### createNewAdmin()
This controller creates a new admin account.
#### test_createNewAdmin()

```python
 def test_createNewAdmin(self):
        admin1 = createNewAdmin("Frinze", "Password", "Email@gmail.com")
        user1 = createNewUser("Sarup", "SomePass", "Email2@gmail.com")
        all = User.query.all()

        self.assertTrue(admin1.is_admin())
        self.assertFalse(user1.is_admin())
```
This test simulates the creation of one admin user account and a normal user account. Then it tests if the account created is an admin account.


