""" Defines data structures to use to read and write to tables """

from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """ Defines data structure for reading and writing to users table """

    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        """ Generates password hash from password """
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """ Compares password hash with password """
        return check_password_hash(self.pwdhash, password)
