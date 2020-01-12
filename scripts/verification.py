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

# Then query for documents
services_list = db.collection(u'services')


class veriForm(FlaskForm):
    code = StringField("verification code", validators=[DataRequired()], render_kw={"placeholder": "required"})
    submit = SubmitField("submit")

@app.route("/verification",methods=['GET','POST'])
def verification_req():
    form = veriForm()
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    if form.validate_on_submit():
        try:
            userSubmittedCode = int(form.code.data)
        except:
            return redirect("/verification?service_id=" + serviceID + "&customer_id=" + customerID)
        user = services_list.document(serviceID).collection("customers").document(customerID)
        if user.get().to_dict()['vericode'] == userSubmittedCode and userSubmittedCode != -1:
            user.update({u'vericode': -1})
            session['phone'] = user.get().to_dict()['phone_number']
            return redirect("/status?service_id=" + serviceID + "&customer_id="+customerID)
        else:
            print("Wrong code")
            return redirect("/verification?service_id=" + serviceID + "&customer_id=" + customerID)
    return render_template("verification.html",form=form)

def getUser(phone):
    for service in services_list:
        for user in service.collection("customers"):
            user = user.to_dict()
            if user['phone'] == phone:
                user['service'] = service.id
                user['id'] = user.id
                return user
    return -1