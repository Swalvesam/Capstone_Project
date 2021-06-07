""" Models for capstone project"""

from flask_sqlalchemy import SQLAlchemy
#unable users to login/logout
from flask_login import UserMixin

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


class Saved_homes(db.Model):
    """Homes saved by User"""
    # def __init__(self):
    #     homes_to_save = self.request.get('homes_to_save', allow_multiple=True)
    
    #     return homes_to_save

    __tablename__ = "saved_homes"

    saved_home_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rm_property_id = db.Column(db.String)
    nickname = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    

    user = db.relationship("User", backref="saved_homes")

    def __repr__(self):
        """Show info about Saved Homes"""
        return f'<Saved_home_id: {self.saved_home_id} Nickname = {self.nickname} Latitude = {self.latitude}>'

    



# class Saved_businesses(db.Model):
    # """ Businesses saved by user"""

# class Home_notes(db.Model):
#     """User notes about home"""

# class Business_notes(db.Model):
#     """User notes about business"""




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