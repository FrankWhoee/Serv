import requests
import os
import json
import datetime
import time
import timeit
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from os import environ
from app import *

@app.route("/confirmation")
def confirmation_req():
    reservationTimeout = 10
    return render_template('confirmation.html', partySize=partySize, wait=wait, reservationTimeout=reservationTimeout)

