from app import db
from app.models import *


# Used To Add Changes To Database
def commitToDatabase(item):
    db.session.add(item)
    db.session.commit()

def createNewUser(username, password, email):
    user = User(username, email,password)
    commitToDatabase(user)

def createNewAdmin(username, password, email):
    user = User(username, email.password)
    adminRole = Privileges.query.filter_by(name="Administrator").first()
    user.role = adminRole
    commitToDatabase(user)

# Gets The User Object Once Validated, otherwise returns false
def validateUserLogin(username, password):
    user = User.query.filter_by(username=username).first()
    if (user and user.check_password(password)):
        return user

    return False


