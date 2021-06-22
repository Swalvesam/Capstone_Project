""" Models for capstone project"""

from flask_sqlalchemy import SQLAlchemy
#allows users to login/logout
from flask_login import UserMixin
#need to import for notes classes
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """A user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    #saved_homes = a list of saved homes by user

    def get_id(self):
        """ Override UserMixin.get_id."""
        return str(self.user_id)

    def __repr__(self):
        """Show info about user"""
        return f'<User_id = {self.user_id} First Name = {self.first_name} Email = {self.email}>'

class SavedHomes(db.Model):
    """Homes saved by User"""
    __tablename__ = "saved_homes"

    saved_home_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rm_property_id = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    address = db.Column(db.Text)
    #home_notes = user notes about home

    user = db.relationship("User", backref="saved_homes")

    def __repr__(self):
        """Show info about Saved Homes"""
        return f'<Saved_home_id: {self.saved_home_id} Nickname = {self.nickname} Latitude = {self.latitude}>'

class HomeNotes(db.Model):
    """User notes about home"""   

    __tablename__ = "home_notes"

    home_note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.Date)
    saved_home_id = db.Column(db.Integer, db.ForeignKey('saved_homes.saved_home_id'))

    saved_home = db.relationship("SavedHomes", backref="home_notes")

    def __repr__(self):
        """Show info about Home Notes"""
        return f'<home_note_id: {self.home_note_id} created_at: {self.created_at} saved_home_id: {self.saved_home_id}>'

class SavedBusinesses(db.Model):
    """Businesses saved by user"""

    __tablename__ = "saved_businesses"

    saved_business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    bus_name = db.Column(db.String)
    yelp_id = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user = db.relationship("User", backref="saved_businesses")

    def __repr__(self):
        """ Show info about Saved Businesses"""
        return f'[(bus_name: {self.bus_name}), (latitude: {self.latitude}), (longitude: {self.longitude})]'

def connect_to_db(flask_app, db_uri='postgresql:///users', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('db connected!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)