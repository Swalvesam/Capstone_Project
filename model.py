""" Models for capstone project"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """ A user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, )
    first_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def get_id(self):
        """ Override UserMixin.get_id."""
        return str(self.user_id)

    def __repr__(self):
        """Show info about user"""
        return f'<User_id = {self.user_id} First Name = {self.first_name} Email = {self.email}>'









def connect_to_db(flask_app, db_uri='postgresql:///users', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)