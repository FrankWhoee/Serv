import requests
import os
import json
import datetime
import time
import timeit
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
from os import environ
from app import *

services_list = db.collection(u'services')

class ConfirmationForm(FlaskForm):
    submit = SubmitField('I\'m here!')

@app.route("/confirmation", methods=['GET','POST'])
def confirmation_req():
    customerID = request.args['customer_id']
    serviceID = request.args['service_id']
    user = services_list.document(serviceID).collection("customers").document(customerID)
    if 'phone' not in session or user.get().to_dict()['phone_number'] != session['phone']:
        return redirect("/")
    form = ConfirmationForm()
    if form.validate_on_submit():
        user.delete()

        return redirect("/")
    return render_template('confirmation.html', form=form)

