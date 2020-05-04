import json
from app import app,db
from flask import render_template, redirect, flash, url_for, request
from werkzeug.urls import url_parse
from app.forms import *
from app.controllers import *
from flask_login import current_user, login_user, logout_user
from app.models import Playlist
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
@app.route("/admin")
def adminPage():
    
        return render_template("admin.html", title="Admin Home")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/process', methods=['GET', 'POST'])
def addSong():
    if request.method == 'POST':
        
        data = request.get_json()
        songName = data['songName']
        songID = data['songID']
        prevURL = data['prevURL']
        newSong = Playlist(songName=songName, songID=songID,prevURL=prevURL)
        db.session.add(newSong)
        db.session.commit()
        checkboxval = request.form.get('songName')

        return str(checkboxval)
    else:
        results = Playlist.query.all()
        return render_template('process.html', title='Songs', results=results)

    
@app.route('/handle_data', methods=['POST'])
def handle_data():
    i = request.form.getlist('songName')
    for r in db.session.query(Playlist).filter(Playlist.songName.in_(i)):
        db.session.delete(r)

    db.session.commit()
    return 'success'