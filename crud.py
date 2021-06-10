#for API requests
import requests, json
import os

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import db, User, HomeNotes, SavedHomes, connect_to_db

#for createtime for notes
from datetime import datetime

#Yelp API Key
YELP_API = os.environ['YELP_API_KEY']

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
        #nickname=nickname
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

def saved_home_longitude(bus_saved_home_id):
    """queries SavedHomes using saved_home_id to get longitude"""
    sql = "SELECT longitude FROM saved_homes WHERE saved_home_id = :saved_home_id"

    cursor = db.session.execute(sql,{"saved_home_id": bus_saved_home_id})

    longitude = cursor.fetchone()

    return longitude

def saved_home_latitude(bus_saved_home_id):
    """queries SavedHomes using saved_home_id to get longitude"""
    sql = "SELECT latitude FROM saved_homes WHERE saved_home_id = :saved_home_id"

    cursor = db.session.execute(sql,{"saved_home_id": bus_saved_home_id})

    latitude = cursor.fetchone()

    return latitude

def list_businesses(property_id):
    """Shows businesses near saved home longtitude and latitude"""
    #need to query for longitude and latitude
    saved_home_id = property_id


    #SQL query to get longitude using saved_home_id
    longitude = saved_home_longitude(saved_home_id)

    #SQL query to get latitude using saved_home_id
    latitude = saved_home_latitude(saved_home_id)

    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

     
    headers = {
        'Authorization': 'Bearer %s' % YELP_API

    }
    url = API_HOST + SEARCH_PATH

    params = {'longitude': longitude, 'latitude': latitude}

    business_search_url = API_HOST + SEARCH_PATH

    req=requests.get(business_search_url, params=params,headers=headers)

    data = json.loads(req.content)

    return data
