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
from google.cloud import firestore
import random
from twilio.rest import Client

# Then query for documents
services_list = db.collection(u'services')


# <a href="/cancelPlace?service_id={{ serviceID }}&customer_id={{ customerID }}" class="button-white">Cancel</a>

class phoneForm(FlaskForm):
    phone = StringField("phone", validators=[DataRequired()])
    submit = SubmitField("Login with Phone Number")


@app.route("/", methods=['GET', 'POST'])
def index_req():
    form = phoneForm()
    if form.validate_on_submit():
        user = generateAndSendVericode(form.phone.data)
        if user == -1:
            return redirect("/")
        return redirect("/verification?service_id=" + user['service'] + "&customer_id=" + user['id'])
    return render_template("index.html", form=form)

def generateAndSendVericode(phone):
    account_sid = 'ACabc7043ed30c2bbffa09aa12fbda8e63'
    auth_token = twilioAuth
    client = Client(account_sid, auth_token)

    vericode = random.randint(1000, 9999)
    user = getUser(phone)
    if user != -1:
        print("Phone found.")
        userObject = services_list.document(user['service']).collection("customers").document(user['id'])
        userObject.update({u'vericode': vericode})
    else:
        print("Did not find phone number: " + phone)
        return -1
    message = client.messages \
        .create(
        body="Your verification code is " + str(vericode),
        from_='+16049016042',
        to=phone
    )
    return user

def getUser(phone):
    for service in services_list.stream():
        service = services_list.document(service.id)
        for user in service.collection("customers").stream():
            id = user.id
            user = user.to_dict()
            if user['phone_number'] == phone:
                user['service'] = service.id
                user['id'] = id
                return user
    return -1
