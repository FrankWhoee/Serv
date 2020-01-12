import requests
import os
import json
import datetime
import time
from google.cloud import firestore
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField, IntegerField, FormField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email
from os import environ
from app import *

class CreateMerchantForm(FlaskForm):
    name = StringField("Organization Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = IntegerField("Phone Number", validators=[DataRequired(), InputRequired()])
    service_capacity = IntegerField("Service Capacity", validators=[DataRequired(), InputRequired()])
    merchant_type = SelectField(u"Merchant Type", choices=[('serv', 'Service'), ('rest', 'Restaurant')])
    submit = SubmitField("Register")

@app.route("/mSignUp", methods=['GET', 'POST'])
def merchantSignUp_req_get():
    # session['email'] = "bobbillyjoe@gmail.com"
    services = db.collection(u'services').stream()
    form = CreateMerchantForm()
    if form.validate_on_submit():
        max = -1
        for service in services:
            if int(service.id) > max:
                max = int(service.id)
        max = max + 1
        print("max" + str(max))
        data = {
            u'name' : form.name.data,
            u'email' : form.email.data,
            u'phone_number' : form.phone_number.data,
            u'merchant_type' : form.merchant_type.data,
            u'service_capacity' : form.service_capacity.data,
        }
        # db.collection('services').document(str(max)).set(data)
        db.collection('services').document(str(max)).set(data)
        flash('New Merchant requested with name {}, email {}, phone number {}'.format(
            form.name.data, form.email.data, form.phone_number.data))
        return redirect("/mgmt?mid="+str(max))
        # return redirect("/mgmt?mid="+merchant)
    return render_template("merchantSignUp.html", form=form)