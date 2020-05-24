# CITS3403-Project2
### "Spotimania"
Aditya Gupta, Frinze Lapuz, Hadi Navabi, Sarup Parajuli

## Table of Contents
1. [Introduction](#introduction)
2. [Assessment Mechanism](#Assessment-Mechanism)
3. [App Architecture](#App-Architecture)
4. [App Launching](#App-Launching)
5. [App Testing](#App-Testing)
6. [Design Process](#Design-Process)

## Introduction 
"Spotimania" is a web application based on the Flask server side rendering micro-framework.
The inspiration for this app comes from the Spotify API which has been used here to create song quizzes for anyone who registers into the application with a personal account. The user is then able to play certain pre-made playlists with multiple people in real-time (through sockets). The quiz itself will require the user to guess the name and the artist for the 30 second demo of the song, and at the end of each question they will receive instant feedback comprising of the correct answers and the scores of all the users that are playing together.

After all the questions have been answered, the user can then click on the results page to see his/her full history of results of every playlist that has been attempted by them. The application also provides administration privileges that allows an admin to add/delete/customise playlists that are available to users. This application provides an excellent and fun quiz for both music lovers and just the casual listener to not only test their knowledge of certain music genres, artists, etc, but also a chance to delve into different music cultures.

## Assessment Mechanism
Spotimania uses 'fuzzy matching' of short answers as its primary assessment mechanism. The python module of 'fuzzywuzzy' has been imported into the flask application which is then used to check if the short answer provided by the user obtains a similarity score of greater than 80/100 based on the fuzzy matching algorithm when compared to the actual answer. We have chosen 80 as our benchmark as when testing the fuzzy algorithm, we found it is quite sensitive in scenarios when even a single letter has been accidentally left out or misspelt compared to the answer and we did not wish to penalise users based on minor spelling errors if it was clear they had identified the correct answer.

## App Architecture (Flask)
This application has been constructed using the python Flask micro-framework MVC. In terms of the Model View Controller Architecture, in our application, the model is represented by the SQLite database and SQLAlchemy, the View is represented by the server-side rendering template of jinja2 which assembles the HTML static content based on the request and the Controller is represented by the Python Flask library.

## App Launching
As with most Flask applications, launching this application requires running the Flask package using `$ flask run` in the directory of the application which will then result in the application being hosted on a local server, usually: http://127.0.0.1:5000/. However, Spotimania has also been deployed on Heroku, and therefore can be accessed directly from the web via the link: https://spotimania.herokuapp.com/.

A more comprehensive guide to setting up the Flask environment and launching the app is listed below:

#### Python prerequisite

Download and install [python 3.8](https://www.python.org/downloads/)

#### Virtual environment

Download virtualenv
```bash
$ pip install virtualenv
```
If you have multiple versions of python installed, please run `pip3` instead

A virtual environment ensure everyone working on this project will have the same dependencies
installed and avoid the "it worked on my machine" bug. Create a new virtualenv with
```bash
$ virtualenv env
```
If you have multiple versions of python installed, run:
```bash
$ virtualenv -p python3.8 env
```
To activate the virtual environment, run
```bash
$ source env/bin/activate
```
You will need to run this command every time you run/develop this application.

#### Requirements
Installing all relevant requirements/packages:
```bash
$ pip install -r requirements.txt
```

#### Running Flask
```bash
$ flask run
```
## App Testing
Our application has been constructed with testers for all the essential controllers that are based on the CRUD operations of the models. To run the tests, we can simply type `python tests/test.py` in the directory of the application as all of our test are contained in the test.py file. Some of the controllers that are written are:
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

## Design Process
The planning and designing prior to development is important to prioritise high value objectives as well as the collaboration of multiple developers involved. Here are the design decisions that were involved in the planning process:

#### App Functionality
The app was developed to allow people of all ages to play a quiz-type game online together with friends/family regarding a certain topic that will appeal to many users. Having discovered the existence of the Spoitfy API, what better way to construct a music quiz! 

The Spotify API allows for the searching of songs and artists which contain multiple data such as a "preview URL", cover image, song name as well as the artist name. Using this API data, we have implemented the following functionalities:
- Song/artist guessing quiz
- Adding of songs to custom playlists
- Real-time multiplayer quiz
- Viewing of results from quizzes
- Admin privileges to register playlists

#### Page Designs/Mock-ups
Our selection of pages in our application consists of
- Central homepage
- A quizpage
- A playlist page
- A results page
- Pages to allow for registration and login
- Hidden page for admin registration.

Some of our mockups include:

![Playlist List](https://user-images.githubusercontent.com/62584922/82750171-ddf0c380-9de0-11ea-8dd2-6b1f81499a9b.png)
![Playlist Admin](https://user-images.githubusercontent.com/62584922/82750173-e1844a80-9de0-11ea-8c5c-775a815a0be5.png)
![ResultsPage](https://user-images.githubusercontent.com/62584922/82750174-e2b57780-9de0-11ea-88eb-e39ad84182ed.png)
![Guess the song](https://user-images.githubusercontent.com/62584922/82750175-e2b57780-9de0-11ea-8dc0-450b8536fbd7.png)
![Adding New Song](https://user-images.githubusercontent.com/62584922/82750176-e34e0e00-9de0-11ea-9624-25fec496a45d.png)

#### Database Schema
The app requires the following data relationships:
- A User can either an admin or normal user
- A user can play many playlists
- A playlist can be played by many users
- A played playlist by a user is called "results"
- A single result will have many attempts for different songs
- A playlist can have many songs
- A song can belong to many playlists

These relationships can be modelled by the following entity relationship diagram:
![Entity Relationship Diagram](https://user-images.githubusercontent.com/62584922/82749902-fd86ec80-9dde-11ea-9922-6475d63bb051.png)
