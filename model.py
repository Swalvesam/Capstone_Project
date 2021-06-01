""" Models for capstone project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ A user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, )
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        """Show info about user"""
        return f'<User_id = {self.user_id} Email = {self.email}>'


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')
    

if __name__ == '__main__':
    from server import app

    connect_to_db(app)