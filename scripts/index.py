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
    submit = SubmitField("submit")


@app.route("/", methods=['GET', 'POST'])
def index_req():
    form = phoneForm()
    if form.validate_on_submit():
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = 'ACabc7043ed30c2bbffa09aa12fbda8e63'
        auth_token = twilioAuth
        client = Client(account_sid, auth_token)

        vericode = random.randint(1000, 9999)
        user = getUser(form.phone.data)
        print(user)
        if user != -1:
            print("Phone found.")
            userObject = services_list.document(user['service']).collection("customers").document(user['id'])
            userObject.update({u'vericode': vericode})
        else:
            print("Did not find phone number: " + form.phone.data)
            return redirect("/")
        message = client.messages \
            .create(
            body="Your verification code is" + str(vericode),
            from_='+16049016042',
            to=form.phone.data
        )
        return redirect("/verification?service_id=" + user['service'] + "&customer_id" + user['id'])
    return render_template("index.html", form=form)


def getUser(phone):
    for service in services_list.stream():
        for user in service.collection("customers"):
            user = user.to_dict()
            if user['phone'] == phone:
                user['service'] = service.id
                user['id'] = user.id
                return user
    return -1
