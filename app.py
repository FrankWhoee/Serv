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
from scripts import confirmation, lineStatus, payment, services, landingTap

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = '\xf0"b1\x04\xe0.[?w\x0c(\x94\xcdh\xc1yq\xe3\xaf\xf2\x8f^\xdc'


# Begin send assets
@app.route('/img/<path>')
def send_assets(path):
    return send_from_directory('img', path)


@app.route('/css/<path>')
def send_style(path):
    return send_from_directory('css', path)


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('js', path)

# End send assets

# Begin send HTML file via route

@app.route('/tap')
def tap_route():
    return landingTap.get()

@app.route('/confirmation')
def confirmation_route():
    return confirmation.get()

@app.route('/status')
def lineStatus_route():
    return lineStatus.get()

@app.route('/payment')
def payment_route():
    return payment.get()

@app.route('/services')
def services_route():
    return services.get()