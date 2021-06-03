"""Server for Capstone Project"""

from flask import Flask
#Allow users to log in/manage login information
from flask_login import LoginManager, login_user, login_required, logout_user

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import jinja2

#for API requests
import requests, json

from model import connect_to_db, User, db

app = Flask(__name__)
app.secret_key = "secret-key"
#app.jinja_env.undefined = StrictUndefined

#creates LoginManager and attaches to Flask app instance
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def homepage():
    """View Homepage"""

    return render_template('homepage.html')

# #callback for login_manager.user_loader
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

    return render_template('users.html')

@app.route('/home_search', methods=["GET", "POST"])
def home_search():
    """Allows users to search for homes for sale"""

    URL = "https://realty-mole-property-api.p.rapidapi.com/saleListings"

    HEADERS = {
    'x-rapidapi-key': "facca4055emshcb21e87d3c94e12p19e6c5jsn13f7b8426702",
    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com"
    }

    address = request.form.get("street_address")
    city = request.form.get("city")
    state = request.form.get("state")
    bedrooms = request.form.get("bedrooms")
    bathrooms = request.form.get("bathrooms")
    
    querystring = {"bedrooms":bedrooms, 
                    "bathrooms": bathrooms, 
                    "city": city,
                    "state": state}


    response = requests.request("GET", URL, headers=HEADERS, params=querystring)
    
    data = json.loads(response.content)

    for d in data:
        print("*"* 20)
        print(d["rawAddress"])
        print("*" * 20) 
    

    return render_template('homes.html', data=data)


@app.route('/homes')
def homes():
    """ View and search for homes"""

    return render_template('homes.html')

# @app.route('/businesses')
# def businesses():
#     """ View businesses"""

#     return render_template('/businesses.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')



