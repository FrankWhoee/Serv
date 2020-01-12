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

# Then query for documents
services_list = db.collection(u'services')


@app.route("/status")
def lineStatus_req():
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    print(customerID)
    print(serviceID)
    waitedTime = int(time.time()) - int(
        services_list.document(serviceID).collection("customers").document(customerID).get().to_dict()['enqueue_time'])
    waitedTime = str(datetime.timedelta(seconds=waitedTime))
    print(waitedTime)
    return render_template("lineStatus.html", avgTime="4:20", waitedTime=waitedTime,
                           place=getPlace(serviceID, customerID))

def getAvgTime(serviceID):
    customers = services_list.document(serviceID).collection("customers").stream()
    temp = []
    for user in customers:
        id = user.id
        user = user.to_dict()
        user['id'] = id
        temp.append(user)

def getPlace(serviceID, customerID):
    customers = services_list.document(serviceID).collection("customers").stream()
    temp = []
    for user in customers:
        id = user.id
        user = user.to_dict()
        user['id'] = id
        temp.append(user)
    temp.sort(key=sortLine)
    i = 0
    print(temp)
    for user in temp:
        if user['id'] == customerID:
            return i
        i += 1
    return -1


def sortLine(a):
    print(int(a['enqueue_time']))
    return int(a['enqueue_time'])
