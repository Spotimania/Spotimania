from app import db
from app.models import *


# Used To Add Changes To Database
def commitToDatabase(item):
    db.session.add(item)
    db.session.commit()

# User Controllers
def getAdminRole():
    adminRole = Privileges.query.filter_by(name="Administrator").first()
    if (adminRole):
        return adminRole
    adminRole = Privileges("Administrator")
    commitToDatabase(adminRole)
    return adminRole

def createNewUser(username, password, email):
    user = User(username.strip(), email.strip(),password.strip())
    commitToDatabase(user)
    return user

def createNewAdmin(username, password, email):
    adminRole = getAdminRole()
    user = User(username.strip(), email.strip(),password.strip(),adminRole)
    commitToDatabase(user)
    return user

# Gets The User Object Once Validated, otherwise returns false
def validateUserLogin(username, password):
    user = User.query.filter_by(username=username.strip()).first()
    if (user and user.check_password(password)):
        return user

    return False

def isUsernameTaken(username):
    user = User.query.filter_by(username=username.strip()).first()
    return  bool(user)

def isEmailTaken(email):
    user = User.query.filter_by(email=email.strip()).first()
    return bool(user)


