import requests
import os
import json
import datetime
import time
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from os import environ
from app import *
from firebase import Firebase

config = {
  "apiKey": firebaseAPIKey,
  "authDomain": "serv-91a70.firebaseapp.com",
  "databaseURL": "https://serv-91a70.firebaseio.com/"
}

firebase = Firebase(config)
# Get a reference to the database service
db = firebase.database()

# data to save
data = {
    "name": "Joe Tilsed"
}

# Pass the user's idToken to the push method
results = db.child("users").push(data, user['idToken'])
@app.route("/status")
def lineStatus_req():


    return render_template("lineStatus.html", avgTime="4:20", waitedTime="2:00", place=5)


