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
from wtforms import ValidationError

class LogInForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),InputRequired(), Email()], render_kw={"placeholder": "required"})
    password = PasswordField("password", validators=[DataRequired()], render_kw={"placeholder": "required"})
    submit = SubmitField('continue 🡆')
    services = db.collection(u'services').stream()


@app.route('/mLogIn', methods=["GET", "POST"])
def merchantLogin_req_get():
    form = LogInForm()
    services = db.collection(u'services').stream()
    if form.validate_on_submit():
        for service in services:
            if service.get('email') == form.email.data and service.get('pass') == form.password.data:
                # return redirect("/tap?service_id=71")
                service_id = service.id
                session['email'] = form.email.data
                return redirect("/mAirtable?service_id="+service_id)
        form.submit.errors.append('merchant error')
        return render_template("merchantLogIn.html", form=form)
    return render_template("merchantLogIn.html", form=form)
        