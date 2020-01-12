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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


config = {
    "apiKey": firebaseAPIKey,
    "authDomain": "serv-91a70.firebaseapp.com",
    "databaseURL": "https://serv-91a70.firebaseio.com/",
    "storageBucket": "serv-91a70.appspot.com"
}

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': firebaseProjectID,
})

db = firestore.client()

@app.route("/status")
def lineStatus_req():
    doc_ref = db.collection(u'services').document('69')

    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except Exception as e:
        print("Error, no such document.")
        print(e)
    return render_template("lineStatus.html", avgTime="4:20", waitedTime="2:00", place=5)
