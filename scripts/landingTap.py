import requests
import os
import json
import datetime
import time
from google.cloud import firestore
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField, IntegerField, FormField
from wtforms.validators import DataRequired, InputRequired
from os import environ
import phonenumbers
from app import *

class EnterQueueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()], render_kw={"placeholder": "required"})
    party_size = IntegerField('party size', validators=[DataRequired(),InputRequired()], render_kw={"value": 1, "placeholder": "required"})
    phone_number = StringField('phone number', validators=[DataRequired(),InputRequired()], render_kw={"placeholder": "required"})
    submit = SubmitField('continue 🡆')


@app.route("/tap", methods=['GET', 'POST'])
def landingTap_req_get():
    serviceID = request.args['service_id']
    merchantRef = db.collection("services").document(serviceID).collection("customers")
    form = EnterQueueForm()
    if form.validate_on_submit():
        customers = merchantRef.stream()
        numCustomers = 0
        for customer in customers:
            numCustomers = numCustomers + 1
        newData = {
            u'name'  : form.name.data,
            u'enqueue_time' : int(time.time()),
            u'phone_number' : str(form.phone_number.data),
            u'party_size' : form.party_size.data,
            u'customer_id' : numCustomers,
            u'confirmed' : False,
            u'vericode': -1,
        }
        merchantRef.document(str(numCustomers)).set(newData)
        print(numCustomers)
        flash('Login requested for user {}, phone number {}'.format(
            form.name.data, form.phone_number.data))
        return redirect("/status?service_id="+serviceID+"&customer_id="+str(numCustomers))
    return render_template("landingTap.html", form=form, serviceID=serviceID)
