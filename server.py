""" Server for Capstone Project"""

from flask import Flask

from flask import (Flask, render_template, request, flash, session,
                   redirect)
import jinja2

from model import connect_to_db

app = Flask(__name__)
app.secret_key = "secret-key"

#app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View Homepage"""

    render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    """Allows users to login """
    # if returning user submit button takes to user homepage 
    #     render_template('users.html')
    # elif if information entered incorrectly have user try again

    # else need to create a user 
 



   


# @app.route('users')
# def users():
#     """ View users profile """

#     render_template('users.html')

# @app.route('homes')
# def homes():
#     """ View and search for homes"""

#     render_template('homes.html')

# @app.route('businesses')
# def businesses():
#     """ View businesses"""

#     render_template('businesses.html')

# @app.route('maps')
# def maps():
#     """View homes and businesses on map"""

#     render_template('maps.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
