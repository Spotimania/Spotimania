import json
from app import app,db
from flask import render_template,redirect,flash
from app.forms import *
from app.controllers import *

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", index=True)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if (form.validate_on_submit()):
        userObject = validateUserLogin(form.username.data,form.password.data)
        if(userObject):
            flash("You are successfully logged in", "success")
            return redirect("/index")
        else:
            flash("Sorry, Your username or password is incorrect","danger")

    return render_template("login.html", title="Login", form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if (form.validate_on_submit()):
        print("USER CREATING")
        createNewUser(form.username.data, form.password.data, form.email.data)
        flash("You are successfully registered", "success")
        return redirect("/index")
    return render_template("register.html", title="Register", form=form)
