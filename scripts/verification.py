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
from wtforms import ValidationError

# Then query for documents
services_list = db.collection(u'services')


class veriForm(FlaskForm):
    code = StringField("code", validators=[DataRequired()])
    submit = SubmitField("submit")

    def validate_code(self, field):
        try:
            userSubmittedCode = int(self.code.data)
        except:
            print("not int")
            raise ValidationError("Non numerical code")
        serviceID = request.args['service_id']
        customerID = request.args['customer_id']
        user = services_list.document(serviceID).collection("customers").document(customerID)
        if user.get().to_dict()['vericode'] == userSubmittedCode and userSubmittedCode != -1:
            print("success")
        else:
            print("other")
            raise ValidationError("other issues")


@app.route("/verification",methods=['GET','POST'])
def verification_req():
    form = veriForm()
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    if form.validate_on_submit():
        return redirect("/status?service_id=" + serviceID + "&customer_id="+customerID)
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