#for API requests
import requests, json
import os

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import db, User, HomeNotes, SavedHomes, SavedBusinesses, connect_to_db

#for createtime for notes
from datetime import datetime, date

#Yelp API 
YELP_API = os.environ['YELP_API_KEY']

def register_new_user(first_name,email,password):
    """creates a new user"""

    new_user = User(first_name=first_name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user

def save_new_home(user_id, rm_property_id, longitude, latitude, address):
    """Creates a new saved home"""
    home = SavedHomes(
        user_id = user_id,
        rm_property_id = rm_property_id,
        longitude=longitude,
        latitude=latitude,
        address=address,
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

    note = HomeNotes(body=body, created_at = date.today(), saved_home_id=saved_home_id)

    db.session.add(note)
    db.session.commit()

    return note
    
def remove_home_note(home_note_id):
    """removes note on saved home"""
    
    note = HomeNotes.query.filter_by(home_note_id=home_note_id).first()

    db.session.delete(note)
    db.session.commit()

    return note

def saved_home_longitude(saved_home_id):
    """queries SavedHomes using saved_home_id to get longitude"""

    sql = "SELECT longitude FROM saved_homes WHERE saved_home_id = :saved_home_id"

    cursor = db.session.execute(sql,{"saved_home_id": saved_home_id})

    longitude = cursor.fetchone()

    return longitude

def saved_home_latitude(saved_home_id):
    """queries SavedHomes using saved_home_id to get longitude"""

    sql = "SELECT latitude FROM saved_homes WHERE saved_home_id = :saved_home_id"

    cursor = db.session.execute(sql,{"saved_home_id": saved_home_id})

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

    # TODO furture stuff save things we got back to the db and filter searches we already have data for

    headers = {
        'Authorization': 'Bearer %s' % YELP_API

    }
    url = API_HOST + SEARCH_PATH

    params = {'longitude': longitude, 'latitude': latitude}

    business_search_url = API_HOST + SEARCH_PATH

    req=requests.get(business_search_url, params=params,headers=headers)

    data = json.loads(req.content)
    print("*****************")
    print(longitude)

    return data

def save_new_business(user_id, bus_name, yelp_id, latitude, longitude):
    """creates a new saved business"""

    business = SavedBusinesses(
        user_id = user_id,
        yelp_id = yelp_id,        
        bus_name = bus_name,
        latitude = latitude,
        longitude = longitude
        )

    db.session.add(business)
    db.session.commit()

    return business

def remove_saved_business(yelp_id):
    """removes saved_business"""
    saved_business = SavedBusinesses.query.filter_by(yelp_id=yelp_id).first()

    db.session.delete(saved_business)
    db.session.commit()
    
    return saved_business

def get_address(saved_home_id):
    """To show home address on home_info page"""

    sql = "SELECT address FROM saved_homes WHERE saved_home_id= :saved_home_id"

    cursor = db.session.execute(sql,{"saved_home_id": saved_home_id})

    old_address = cursor.fetchone()
    
    address = " ".join(old_address)

    return address
