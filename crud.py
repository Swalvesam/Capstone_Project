
from model import db, User, HomeNotes, SavedHomes, connect_to_db

#for createtime for notes
from datetime import datetime

def register_new_user(first_name,email,password):
    """creates a new user"""

    new_user = User(first_name=first_name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user

def save_new_home(rm_property_id,user_id,longitude,latitude):
    """Creates a new saved home"""
    home = SavedHomes(
        rm_property_id = rm_property_id,
        user_id = user_id,
        longitude=longitude,
        latitude=latitude,
        # nickname=nickname
        )
    
    db.session.add(home)
    db.session.commit()

    return home

def remove_saved_home(rm_property_id):
    """removes saved home"""
    saved_home = SavedHomes.query.filter_by(rm_property_id=rm_property_id).first()

    db.session.delete(saved_home)
    db.session.commit()
    
    return saved_home

def create_home_note(body,saved_home_id):
    """Creates a new home note on saved home"""

    note = HomeNotes(body=body, created_at = datetime.today(), saved_home_id=saved_home_id)

    db.session.add(note)
    db.session.commit()

    return note
    
def remove_home_note(home_note_id):
    """removes note on saved home"""
    
    note = HomeNotes.query.filter_by(home_note_id=home_note_id).first()

    db.session.delete(note)
    db.session.commit()

    return note
