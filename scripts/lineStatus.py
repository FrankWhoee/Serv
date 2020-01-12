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
    waitedTime = services_list.document(serviceID).get().to_dict()[customerID]

    return render_template("lineStatus.html", avgTime="4:20", waitedTime=waitedTime, place=getPlace(serviceID,customerID))


def getPlace(serviceID, customerID):
    customers = services_list.document(serviceID).get().to_dict()
    temp = []
    for user in customers.keys():
        customers['id'] = user
        temp.append(customers[user])
    temp.sort(key=sortLine)
    i = 0
    for user in temp:
        if user['id'] == customerID:
            return i
        i += 1
    return -1


def sortLine(a, b):
    return int(a['enqueue_time']) - int(b['enqueue_time'])
