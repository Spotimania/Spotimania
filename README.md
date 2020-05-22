# CITS3403-Project2

## Introduction
"Spotimania" is a web application based on the Flask server side rendering micro-framework.
The inspiration for this app comes from the Spotify API which has been used here to create song quizzes for anyone who registers into the application with a personal acccount. The user is then able to select certain pre-made playlists which have been accessed through the Spotify API as mentioned, and is then required to guess each song in the playlist after a 30 second demo audio of the song. After all the questions have been answered, the user is then able to see his/her results on the results page. The application also provides administration privaleges that allows an admin to add/delete playlists that are available to users. This application provides an excellent and fun quiz for both music lovers and just the casual listener to not only test their knowledge of certain music genres, artists, etc, but also a chance to delve into different music cultures.

## Assessment Mechanism
Spotimania uses 'fuzzy matching' of short answers as its primary assessment mechanism. The python module of 'fuzzywuzzy' has been imported into the flask application which is then used to check if the short answer provided by the user obtains a similarity score of greater than 80/100 based on the fuzzy matching algorithm when compared to the actual answer. We have chosen 80 as our benchmark as when testing the fuzzy algortihm, we found it is quite sensitive in scenarios when even a single letter has been accidentally left out or misspelt compared to the answer and we did not wish to penalise users based on minor spelling errors if it was clear they had indentified the correct answer.

## App Architecture (Flask)
This application has been constructed using the python Flask microframeowork MVC. Flask handles quite a lot of the functionalities needed to run this app, however, as suggested by the 'micro' in microframework, a lot of the decisions such as what database to use, templating engine etc are quite flexible. Due to the quite simple requirements of this app using the spotify API and just needing to store broadly standard user, admin and song data, the SQLite database was used. 

In terms of the Model View Controller Architecture, in our application, the model is represented by the SQLite Database, the View is represented by the server-side rendering template of jinja2 which assembles the HTML static content based on the request and the Controller is repreneted by the Python Flask library.


## Functionality
- Song Playing
- Guessing / Fuzzy Matching / Multi-choice
- Recording of Results
- Recording of Songs Available To Be Played
- Administrator Implementation Quiz
   - backend server
- Random Song Quiz
   - popularity
   - checking of the preview url
- Login/Registration of Account
- Guess Mode

## Features
- Multiplayer / Realtime
