"""Server for Capstone Project"""

from flask import Flask
#Allow users to log in/manage login information
from flask_login import LoginManager, login_user, login_required

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import jinja2

from model import connect_to_db, User

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

    if password == user.password:
        # Call flask_login.login_user to login a user
        login_user(user)

        flash("YAY! You're Logged in!")
    
        return redirect("/users")
    
    flash("Email or Password invalid. Please try again.")
    
    return redirect("/")

@app.route("/register", methods=["POST"])

 


@app.route('/users')
def users():
    """ View users profile """

    return render_template('users.html')

@app.route('/homes')
def homes():
    """ View and search for homes"""

    return render_template('homes.html')

# @app.route('/businesses')
# def businesses():
#     """ View businesses"""

#     return render_template('/businesses.html')

# @app.route('/maps')
# def maps():
#     """View homes and businesses on map"""

#     return render_template('/maps.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')



# Hi, Im in Malala C, I'm getting a NameError User not defined 