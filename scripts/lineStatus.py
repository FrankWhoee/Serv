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
from twilio.rest import Client

# Then query for documents
services_list = db.collection('services')


class LineStatusForm(FlaskForm):
    confirm = SubmitField('confirm')
    cancel = SubmitField('cancel')


@app.route("/status", methods=['GET', 'POST'])
def lineStatus_req():
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    print(customerID)
    print(serviceID)
    try:
        user = services_list.document(serviceID).collection("customers").document(customerID).get().to_dict()
        if 'phone' not in session or user['phone_number'] != session['phone']:
            print("Not logged in.")
            return redirect("/")
        waitedTime = int(time.time()) - int(user['enqueue_time'])
        waitedTime = str(datetime.timedelta(seconds=waitedTime))
    except Exception as e:
        print("Error occurred in calculating waittime")
        print(e)
        return redirect("/")

    print(waitedTime)
    form = LineStatusForm()
    partyNum = user['party_size']
    place = getPlace(serviceID, customerID)

    if form.validate_on_submit():
        print("button pressed")
        if form.confirm.data and place == 0:
            return redirect("/confirmation?service_id=" + serviceID + "&customer_id=" + customerID)
        if form.cancel.data:
            return delete_customer()

    return render_template("lineStatus.html", avgTime="-- minutes", waitedTime=waitedTime,
                           place=place, partyNum=partyNum, form=form, serviceID=serviceID, customerID=customerID, service=services_list.document(serviceID).get().to_dict()['name'])


def getAvgTime(serviceID):
    customers = services_list.document(serviceID).collection("customers").stream()
    sum = 0
    count = 0
    for user in customers:
        waitedTime = int(time.time()) - int(user.to_dict()['enqueue_time'])
        sum += waitedTime
        count += 1
    result = str(datetime.timedelta(seconds=sum / count))
    return (result[0:result.find(":") - 1], result[result.find(":")+1:result.rfind(":")])


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


@app.route("/cancelPlace")
def delete_customer():
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    services_list.document(serviceID).collection("customers").document(customerID).delete()
    remindSMSConfirm(serviceID)
    return redirect("/")

@app.route("/getStats")
def returnStats():
    serviceID = request.args['service_id']
    customerID = request.args['customer_id']
    user = services_list.document(serviceID).collection("customers").document(customerID).get().to_dict()
    if 'phone' not in session or user['phone_number'] != session['phone']:
        return redirect("/")
    waitedTime = int(time.time()) - int(user['enqueue_time'])
    serviceID = request.args['service_id']
    results = {}
    results['avgTime'] = getAvgTime(serviceID)
    results['wTime'] = str(datetime.timedelta(seconds=waitedTime))
    results['place'] = str(getPlace(serviceID, customerID))
    return json.dumps(results)


def remindSMSConfirm(serviceID):
    customers = services_list.document(serviceID).collection("customers").stream()
    temp = []
    for user in customers:
        id = user.id
        user = user.to_dict()
        user['id'] = id
        temp.append(user)
    temp.sort(key=sortLine)
    phone = temp[0]['phone_number']

    account_sid = 'ACabc7043ed30c2bbffa09aa12fbda8e63'
    auth_token = twilioAuth
    client = Client(account_sid, auth_token)

    try:
        message = client.messages \
            .create(
            body="Hey! You are the next in line for " + services_list.document(serviceID).get().to_dict()['name'] + ".Go to https://team-serv.herokuapp.com/status?service_id="+serviceID + "&customer_id=" + user['id'] + " to confirm your spot.",
            from_='+16049016042',
            to=phone
        )
    except:
        print("Authorization failed.")
        return {"error": "Number is not verified. Twilio account is trial. Upgrade to fix."}
    return user