from app import app, db, controllers
# importing app variable from the app folder

from app.models import *
from app.controllers import *

#Shell Configurations
@app.shell_context_processor
def make_shell_contect():
    return {"ctrl":controllers,"db":db,"User":User,"Privileges":Privileges,"Song":Song,"Playlist_Song":Playlist_Song,"Playlist":Playlist,"Results":Results,"IndividualResults":IndividualResults}