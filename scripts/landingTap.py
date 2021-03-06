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
from app import *
from scripts.index import generateAndSendVericode
from scripts.index import getUser

class EnterQueueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()], render_kw={"placeholder": "required"})
    party_size = IntegerField('party size', validators=[DataRequired(), InputRequired()],
                              render_kw={"value": 1, "placeholder": "required"})
    phone_number = StringField('phone number', validators=[DataRequired(), InputRequired()],
                               render_kw={"placeholder": "required"})
    submit = SubmitField('continue 🡆')


@app.route("/tap", methods=['GET', 'POST'])
def landingTap_req_get():
    serviceID = request.args['service_id']
    merchantRef = db.collection("services").document(serviceID).collection("customers")
    form = EnterQueueForm()
    if form.validate_on_submit():
        customers = merchantRef.stream()
        if int(db.collection('services').document(serviceID).get(field_paths={'service_capacity'}).to_dict()[
                   'service_capacity']) < form.party_size.data:
            return render_template("error.html", error="Your party size is too big for the merchant.")
        numCustomers = 0
        for customer in customers:
            numCustomers = numCustomers + 1
        newData = {
            u'name': form.name.data,
            u'enqueue_time': int(time.time()),
            u'phone_number': str(form.phone_number.data),
            u'party_size': form.party_size.data,
            u'customer_id': numCustomers,
            u'vericode': -1,
        }
        phoneUser = getUser(form.phone_number.data)
        if phoneUser != -1:
            return redirect("/status?service_id=" + phoneUser['service'] + "&customer_id=" + phoneUser['id'])

        headers = {
            'Authorization': 'Bearer key1LZY2WzVaGvoLR',
            'Content-Type': 'application/json',
        }

        data = '{\n  "records": [\n    {\n      "fields": {\n        "customer_id": "' + str(
            numCustomers) + '",\n        "party_size": "' + str(
            form.party_size.data) + '",\n        "phone_number": "' + str(
            form.phone_number.data) + '",\n        "name": "' + form.name.data + '",\n        "enqueue_time": "' + time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))) + '",\n  "vericode": "-1"\n      }\n    }]\n}'

        response = requests.post('https://api.airtable.com/v0/appbnu6z63Rg9Dno0/' + serviceID, headers=headers,
                                 data=data)

        merchantRef.document(str(numCustomers)).set(newData)
        print(numCustomers)
        flash('Login requested for user {}, phone number {}'.format(
            form.name.data, form.phone_number.data))
        user = generateAndSendVericode(form.phone_number.data)
        if 'error' in user:
            return render_template("error.html", error=user['error'])
        return redirect("/verification?service_id=" + serviceID + "&customer_id=" + str(numCustomers))
    return render_template("landingTap.html", form=form, serviceID=serviceID, db=db)
