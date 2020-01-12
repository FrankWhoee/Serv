import requests
import os
import json
import datetime
import time
import phonenumbers
from google.cloud import firestore
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField, IntegerField, FormField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Email
from os import environ
from app import *



@app.route('/mgmt')
def merchantManagement_req_get():
    # if 'email' in session:
    services = db.collection('services').stream()
    service_id = request.args["service_id"]
    merchant = None
    tables = []
    users = []
    for service in services:
        if str(service.id) == service_id:
            merchant = service
    for table in db.collection('services').document(service_id).collection('tables').stream():
        tables.append(table)
    for user in db.collection('services').document(service_id).collection('customers').stream():
        users.append(user)
    return render_template('merchantManagement.html', tables=tables, users=users, service_id=service_id, merchant=merchant)
    # return render_template('error.html')
    
    