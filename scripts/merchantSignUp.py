import requests
import os
import json
import datetime
import time
from google.cloud import firestore
from flask import Flask, request, render_template, send_from_directory, session, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, StringField, IntegerField, FormField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Email
from os import environ
from app import *

class CreateMerchantForm(FlaskForm):
    name = StringField("organization name", validators=[DataRequired()], render_kw={"placeholder": "required"})
    email = StringField("email", validators=[DataRequired(), Email()], render_kw={"placeholder": "required"})
    password = PasswordField("password", validators=[DataRequired()], render_kw={"placeholder": "required"})
    phone_number = IntegerField("phone number", validators=[DataRequired(), InputRequired()], render_kw={"placeholder": "required"})
    service_capacity = IntegerField("service capacity", validators=[DataRequired(), InputRequired()], render_kw={"placeholder": "required"})
    merchant_type = SelectField(u"merchant type", choices=[('serv', 'Service'), ('rest', 'Restaurant')])
    submit = SubmitField("register")

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
            u'pass' : form.password.data,
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