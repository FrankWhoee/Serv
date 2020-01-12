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

class LogInForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),InputRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])

def checkLogIn(mail, pass):


@app.route('/mLogIn')
def merchantLogin_req_get():
    # get merchant id
    # find merchant with that id
    # check entered email and pass are correct
    # if yes, move to management page with merchant id and unique id?
    # else, reload page and show errors
    form = LogInForm()
    # merchant_id = request.args['mid']
    services = db.collections("services")

        if form.validate_on_submit():
            for service in services.stream():
                if service.email == form.email.data and service.password = form.password.data:
                    session['email'] = form.email.data
                    break
            
            return redirect("/merchantManagement?service_id="+service_id+"&unid="+str(unid)")