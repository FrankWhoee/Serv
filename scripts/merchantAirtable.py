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

@app.route('/mAirtable', methods=["GET", "POST"])
def merchant_airtable_get():
    serviceID = request.args['service_id']
    link = json.load("serviceAirtableMap.json")
    return render_template("merchantAirtable.html", link=link[serviceID])