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

class EnterQueueForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    party_size = IntegerField('Party Size', validators=[DataRequired(),InputRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired(),InputRequired()])
    submit = SubmitField('Enter Queue')

@app.route("/tap", methods=['GET', 'POST'])
def landingTap_req_get():
    serviceID = request.args['service_id']
    merchantRef = db.collection("services").document(serviceID)
    form = EnterQueueForm()
    if form.validate_on_submit():
        data = {
            u'name'  : form.name.data,
            u'enqueue_time' : firestore.SERVER_TIMESTAMP,
            u'phone_number' : str(form.phone_number.data),
            u"party_size" : form.party_size.data
        }
        merchantRef.update(data)
        flash('Login requested for user {}, phone number {}'.format(
            form.name.data, form.phone_number.data))
        return redirect(url_for('confirmation'))
    return render_template("landingTap.html", form=form, serviceID=serviceID)
