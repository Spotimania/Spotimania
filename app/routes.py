import json
from app import app,db
from flask import render_template, redirect, flash, url_for, request
from werkzeug.urls import url_parse
from app.forms import *
from app.controllers import *
from flask_login import current_user, login_user, logout_user
from flask import jsonify

def redirectToLastVisitedPage():
    next_page = request.args.get('next')
    print(next_page)
    # Allows only redirection to site itself and relative path
    if not next_page or url_parse(next_page).netloc != '':
        print("REDIRECT TO INDEX")
        next_page = url_for('index')
    print(next_page)
    return redirect(next_page)

def redirectTo404():
    return redirect(url_for('page404'),404)

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    print(current_user)
    try:
        print(current_user.role)
    except AttributeError:
        pass
    return render_template("index.html", index=True)

@app.route("/login",methods=["GET","POST"])
def login():
    # PREVENT USER TO LOGIN WHEN LOGIN
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if (form.validate_on_submit()):
        userObject = validateUserLogin(form.username.data,form.password.data)
        if(userObject):
            flash("You are successfully logged in", "success")
            login_user(userObject, remember=form.rememberMe.data)

            return redirectToLastVisitedPage()

        else:
            flash("Sorry, Your username or password is incorrect", "danger")

    return render_template("login.html", title="Login", form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    # PREVENT USER TO REGISTER WHEN LOGIN
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if (form.validate_on_submit()):
        userObject = createNewUser(form.username.data, form.password.data, form.email.data)
        login_user(userObject)
        flash("You are successfully registered", "success")
        return redirect("/index")
    return render_template("register.html", title="Register", form=form)

@app.route("/registerAdmin",methods=["GET","POST"])
def registerAdmin():
    # PREVENT USER TO REGISTER WHEN LOGIN
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterAdminForm()
    if (form.validate_on_submit()):
        if(app.config["ADMIN_KEY"]==form.specialPassword.data):
            userObject = createNewAdmin(form.username.data, form.password.data, form.email.data)
            login_user(userObject)
            flash("You are successfully registered", "success")
            return redirect("/index")
        else:
            flash("Your Admin Key Is Wrong")
    return render_template("register.html", title="Register Admin", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
@app.route('/404')
def page404(error=404):
    return render_template('404.html'), 404


@app.route('/playlists', methods=['GET', 'POST'])
def playlists():

    form = CreateNewPlaylistForm()
    if (form.validate_on_submit()):
        playlistName = form.playlistName.data
        newPlaylist = createNewPlaylist(playlistName)
        return redirect(url_for('playlist',playlistId=newPlaylist.id))

    playlistsCollection = getAllPlaylists();
    return render_template('playlist.html', title='Songs', playlists = playlistsCollection, form=form)

@app.route('/playlist/<playlistId>', methods=['GET', 'POST'])
def playlist(playlistId):
    playlist = getPlaylist(playlistId)
    if (playlist is None):
        return redirectTo404()

    songs = getSongsInPlaylist(playlistId)
    return render_template("admin.html", title="Admin Home",playlist=playlist,songs=songs)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    i = request.form.getlist('songName')
    for r in db.session.query(Song).filter(Song.songName.in_(i)):
        db.session.delete(r)

    db.session.commit()
    return 'success'

@app.route('/quiz/<playlistId>')
def quiz(playlistId):
    print(playlistId)
    return render_template("quiz.html", title="Quiz Page")

@app.route('/results')
def results():
    return render_template("results.html", title="Results Page")