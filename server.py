"""Server for Capstone Project"""

from flask import Flask
#Allow users to log in/manage login information
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import jinja2

#for createtime for notes
from datetime import datetime, date

#for API requests
import requests, json
import os

import crud
from crud import (register_new_user, save_new_home, remove_saved_home, create_home_note, remove_home_note,
                    saved_home_longitude, saved_home_latitude)

from model import connect_to_db, User, db, SavedHomes, HomeNotes

app = Flask(__name__)
app.secret_key = "secret-key"
#app.jinja_env.undefined = StrictUndefined

#Home API Key
HOME_API = os.environ['HOME_SEARCH_API_KEY']

#Yelp API Key
YELP_API = os.environ['YELP_API_KEY']

#creates LoginManager and attaches to Flask app instance
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def homepage():
    """View Homepage"""

    return render_template('homepage.html')

#callback for login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["GET","POST"])
def login():
    """Allows users to login """
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if email == "" or password == "":
        flash("Email or Password invalid. Please try again.")
        return redirect("/") 
    elif password == user.password:
        # Call flask_login.login_user to login a user
        login_user(user)

        flash("YAY! You're Logged in!")
    
        return redirect("/users")
    else:
        flash("Email or Password invalid. Please try again.")
    
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def new_user():
    """Creates a new User"""
    
    #inputs by user to create user
    first_name = request.form.get("first_name")
    email = request.form.get("new_user_email")
    password = request.form.get("new_user_password")
    
    user = User.query.filter(User.email == email).first()
    
    if first_name == "" and email == "" and password == "" :
        return ("Please enter name, email and password to create new user")

    if user:
        #need to fix this to show pop up message
        return ("This email is already in use")
    else:
        #adds new user to database
        crud.register_new_user(first_name,email,password)

        return redirect("/users")
 
@app.route("/logout")
def logout():
    """Allows user to log out"""
    logout_user()
    return redirect("/")

@app.route('/users')
def users():
    """ View users profile """
    #need to pass in saved_homes in order to view them on user dashboard
    saved_homes = SavedHomes.query.filter_by(user_id=current_user.user_id).all()

    return render_template('users.html',saved_homes=saved_homes) 

@app.route('/home_search', methods=["GET"])
def home_search():
    """Allows users to search for homes for sale"""
    #api used for getting homes for sale
    URL = "https://realty-mole-property-api.p.rapidapi.com/saleListings"

    HEADERS = {
    'x-rapidapi-key': HOME_API,
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

    #user inputs to filter search results
    price = request.args.get("max_price")
    address = request.args.get("street_address")
    city = request.args.get("city")
    state = request.args.get("state")
    bedrooms = request.args.get("bedrooms")
    bathrooms = request.args.get("bathrooms")
    
    #default params used by API
    querystring = { "bedrooms":bedrooms, 
                    "bathrooms": bathrooms, 
                    "city": city,
                    "state": state}
    
    #data given back from API request
    response = requests.request("GET", URL, headers=HEADERS, params=querystring)
    
    #changing into JSON in order to loop over data to set by max price
    data = json.loads(response.content)
    
    #also filtering by max price set by user
    filtered_data = []
    for listing in data:
        if listing["price"] <= int(price):
            filtered_data.append(listing)

    if filtered_data == []:
        flash("no homes found, Please try another search")
        return redirect("/users")
    else:
        return render_template('homes.html', data=filtered_data)

@app.route('/return_to_user_dashboard')
def return_to_user_dashboard():
    """Returns user to user dashboard"""

    #buttons located on homes.html and home_info.html

    return redirect("/users")

@app.route('/save_home', methods=["POST"])
@login_required
def save_home_to_user():
    """Saves a home to user dashboard"""
    rm_property_id = request.form.get("rm_property_id")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    # nickname = request.form.get("nickname")
    user_id = current_user.user_id

    saved_home = SavedHomes.query.filter_by(rm_property_id=rm_property_id).first()
    if not saved_home:
        crud.save_new_home(rm_property_id,user_id,longitude,latitude)

    return redirect('/users')

@app.route('/remove_saved_home', methods=["POST"])
@login_required
def remove_saved_home():
    """removes home from saved home table"""
    rm_property_id = request.form.get('remove_saved_home')

    crud.remove_saved_home(rm_property_id)

    return redirect("/users")

@app.route('/view_home_info/<property_id>', methods=["GET","POST"])
@login_required
def view_home_info(property_id):
    """Allows user to view saved home info and businesses near home"""
    saved_home_id = request.form.get("property_id")
    
    business_data = crud.list_businesses(property_id)

    businesses = []

    if business_data != None and "businesses" in business_data and business_data["businesses"] != []: 
        for business in business_data["businesses"]:
            meter_to_mile = 1609.344
            businesses.append(( business["name"],
                                business["image_url"],
                                business["url"],
                                business["categories"],
                                business["rating"],
                                business["coordinates"],
                                round((float(business["distance"])/meter_to_mile),2),
                                "".join([x + " " for x in business["location"]["display_address"]]))) #TODO loop over location info

    else:
        pass
        # TODO something else if we didn't get anything

    home_notes = HomeNotes.query.filter_by(saved_home_id=property_id).all()

    return render_template('home_info.html',saved_home_id=saved_home_id, home_notes=home_notes,property_id=property_id, businesses=businesses)

@app.route('/add_home_note', methods=["POST"])
@login_required
def add_home_note():
    """Allows user to add note to saved home"""

    saved_home_id = request.form.get("property_id")

    body = request.form.get("body")

    crud.create_home_note(body,saved_home_id)
    

    return redirect(f'/view_home_info/{saved_home_id}')

@app.route('/remove_home_note', methods=["POST"])
@login_required
def remove_home_note():
    """Allows user to delete home note"""
   
   #pulled from hidden input, need in order to refresh page after note removal
    saved_home_id = request.form.get("property_id") 

    home_note_id = request.form.get("remove_home_note")
    
    crud.remove_home_note(home_note_id)

    return redirect(f'/view_home_info/{saved_home_id}')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(use_reloader=True, use_debugger=True)
 