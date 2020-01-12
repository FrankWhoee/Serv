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

@app.route('/mLogIn')

def merchantLogin_req_get():
    form = LogInForm()
        if form.validate_on_submit():
            
            return redirect("/merchantManagement?service_id="+service_id+"&unid="+str(unid)")