from app import db
from werkzeug.security import generate_password_hash,check_password_hash

# Define a base model for other database tables to inherit
# Useful for logging purposes
class Base(db.Model):

    __abstract__  = True

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class BaseAutoPrimary(Base):
    __abstract__ = True
    id            = db.Column(db.Integer, primary_key=True)
