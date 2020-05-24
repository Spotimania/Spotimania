# CITS3403-Project2
### "Spotimania"
Aditya Gupta, Frinze Lapuz, Hadi Navabi, Sarup Parajuli

## Table of Contents
1. [Introduction](#intro)
2. [Assessment Mechanism](#assMech)
3. [App Architecture](#appArch)
4. [App Launch](#appLaunch)

## Introduction <a name="intro"></a>
"Spotimania" is a web application based on the Flask server side rendering micro-framework.
The inspiration for this app comes from the Spotify API which has been used here to create song quizzes for anyone who registers into the application with a personal acccount. The user is then able to play certain pre-made playlists with multiple people in real-time (through sockets). The quiz itself will require the user to guess the name and the artist for the 30 second demo of the song, and at the end of each question they will receive instant feedback comprising of the correct answers and the scores of all the users that are playing together.

After all the questions have been answered, the user can then click on the results page to see his/her full history of results of every playlist that has been attempted by them. The application also provides administration privileges that allows an admin to add/delete/customise playlists that are available to users. This application provides an excellent and fun quiz for both music lovers and just the casual listener to not only test their knowledge of certain music genres, artists, etc, but also a chance to delve into different music cultures.

## Assessment Mechanism <a name="assMech"></a>
Spotimania uses 'fuzzy matching' of short answers as its primary assessment mechanism. The python module of 'fuzzywuzzy' has been imported into the flask application which is then used to check if the short answer provided by the user obtains a similarity score of greater than 80/100 based on the fuzzy matching algorithm when compared to the actual answer. We have chosen 80 as our benchmark as when testing the fuzzy algortihm, we found it is quite sensitive in scenarios when even a single letter has been accidentally left out or misspelt compared to the answer and we did not wish to penalise users based on minor spelling errors if it was clear they had identified the correct answer.

## App Architecture (Flask) <a name="appArch"></a>
This application has been constructed using the python Flask microframeowork MVC. Flask handles quite a lot of the functionalities needed to run this app, however, as suggested by the 'micro' in microframework, a lot of the decisions such as what database to use, templating engine etc are quite flexible. Due to the quite simple requirements of this app using the spotify API and just needing to store broadly standard user, admin and song data, the SQLite database was used. 

In terms of the Model View Controller Architecture, in our application, the model is represented by the SQLite Database, the View is represented by the server-side rendering template of jinja2 which assembles the HTML static content based on the request and the Controller is repreneted by the Python Flask library.

## Using Spotimania <a name="appLaunch"></a>
As with most Flask applications, launching this application requires running the Flask package which will then result in the application being hosted on a local server, usually: http://127.0.0.1:5000/. However, Spotimania has also been deployed on Heroku, and therefore can be accessed directly from the web via the link:.
