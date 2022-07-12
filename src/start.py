#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

from flask import Flask, render_template, request
from flask.logging import create_logger

from database import Database

# Create Flask object
APP = Flask(__name__)
LOGGER = create_logger(APP)

# Load initial account data from JSON file
db = Database("mysql://root:globomantics@db/db", "data/initial.json")


@APP.before_request
def before_request():
    """
    Before each request, connect to the database.
    """
    db.connect()
    LOGGER.debug("Connected to database")


@APP.after_request
def after_request(response):
    """
    After each request, disconnect from the database.
    """
    db.disconnect()
    LOGGER.debug("Disconnected from database")
    return response


@APP.route("/", methods=["GET", "POST"])
def index():
    """
    This is a view function which responds to requests for the top-level
    URL. It serves as the "controller" in MVC as it accesses both the
    model and the view.
    """

    # The button click within the view kicks off a POST request ...
    if request.method == "POST":

        # This collects the user input from the view. The controller's job
        # is to process this information, which includes using methods from
        # the "model" to get the information we need (in this case,
        # the account balance).
        acct_id = request.form["acctid"]
        acct_balance = db.balance(acct_id.upper())
        LOGGER.debug("balance for %s: %s", acct_id, acct_balance)

    else:
        # During a normal GET request, no need to perform any calculations
        acct_balance = "N/A"

    # This is the "view", which is the jinja2 templated HTML data that is
    # presented to the user. The user interacts with this webpage and
    # provides information that the controller then processes.
    # The controller passes the account balance into the view so it can
    # be displayed back to the user.
    return render_template("index.html", acct_balance=acct_balance)


if __name__ == "__main__":
    ctx = ("../ssl/cert.pem", "../ssl/key.pem")
    APP.run(host="0.0.0.0", debug=True, use_reloader=False, ssl_context=ctx)    #nosec
