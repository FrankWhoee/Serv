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
    