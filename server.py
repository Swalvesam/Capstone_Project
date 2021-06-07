"""Server for Capstone Project"""

from flask import Flask
#Allow users to log in/manage login information
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import jinja2

#for API requests
import requests, json
import os

from model import connect_to_db, User, db, Saved_homes

app = Flask(__name__)
app.secret_key = "secret-key"
#app.jinja_env.undefined = StrictUndefined

#Home API Key
HOME_API = os.environ['HOME_SEARCH_API_KEY']

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
    
    first_name = request.form.get("first_name")
    email = request.form.get("new_user_email")
    password = request.form.get("new_user_password")
    
    user = User.query.filter(User.email == email).first()
    # if first_name == "" and email == "" and password == "" :
    #     return ("Please enter name, email and password to create new user")

    if user:
        #need to fix this to show pop up message
        return ("This email is already in use")
    else:
        #add's new user to database
        new_user = User(first_name=first_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")
 
@app.route("/logout")
def logout():
    """Allows user to log out"""
    logout_user()
    return redirect("/")

@app.route('/users')
def users():
    """ View users profile """
    saved_homes = Saved_homes.query.filter_by(user_id=current_user.user_id).all()
    return render_template('users.html',saved_homes=saved_homes)

@app.route('/home_search', methods=["GET"])
def home_search():
    """Allows users to search for homes for sale"""

    URL = "https://realty-mole-property-api.p.rapidapi.com/saleListings"

    HEADERS = {
    'x-rapidapi-key': HOME_API,
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

    price = request.args.get("max_price")
    address = request.args.get("street_address")
    city = request.args.get("city")
    state = request.args.get("state")
    bedrooms = request.args.get("bedrooms")
    bathrooms = request.args.get("bathrooms")
    

    querystring = { "bedrooms":bedrooms, 
                    "bathrooms": bathrooms, 
                    "city": city,
                    "state": state}


    response = requests.request("GET", URL, headers=HEADERS, params=querystring)
    
    data = json.loads(response.content)
    
    #also filtering by max price set by user
    filtered_data = []
    for listing in data:
        if listing["price"] <= int(price):
            filtered_data.append(listing)

    return render_template('homes.html', data=filtered_data)

@app.route('/return_to_user_dashboard')
def return_to_user_dashboard():
    """Returns user to user dashboard"""
    return redirect("/users")

@app.route('/save_home', methods=["POST"])
@login_required
def save_home_to_user():
    """saves a home to user dashboard"""
    rm_property_id = request.form.get("homes_to_save")
    # longitude = request.form.get("longitude")
    # latitude = request.form.get("latitude")
    # nickname = request.form.get("nickname")

    saved_home = Saved_homes.query.filter_by(rm_property_id=rm_property_id).first()
    if not saved_home:

        home = Saved_homes(
                rm_property_id = rm_property_id,
                user_id = current_user.user_id,
                # longitude=longitude,
                # latitude=latitude,
                # nickname=nickname
        )
    
        db.session.add(home)
        db.session.commit()

    return redirect('/users')


# @app.route('/businesses')
# def businesses():
#     """ View businesses"""

#     return render_template('/businesses.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(use_reloader=True, use_debugger=True)



