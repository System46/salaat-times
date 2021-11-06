from flask import Flask, render_template, request
from datetime import date, datetime
from geopy.geocoders import Nominatim
from pyIslam.praytimes import (
    PrayerConf,
    Prayer,
    LIST_FAJR_ISHA_METHODS
)
from timezonefinder import TimezoneFinder
import pytz
import requests

app = Flask(__name__)


def checkArg(argName, argType='str'):
    """ Function to check if argument is in request and if it has correct type"""
    if argType:
        if argType == 'str':
            try:
                return request.args.get(argName, type=str)

            except Exception as e:
                return e
        elif argType == 'int':
            try:
                return request.args.get(argName, type=int)
            except Exception as e:
                return e
    else:
        try:
            return request.args.get(argName)
        except Exception as e:
            return e


def checkCity():
    city = checkArg('city', 'str')
    if not city:
        lat, long = checkArg('lat'), checkArg('long')
        if not lat or not long:
            return "missing args city , lat or long"
        else:
            return f"{lat}|{long}"
    else:
        return f"{city}"
@app.route("/praytimes/today", methods=['GET', 'POST'])
def praytimes():
    if request.method == 'POST':
        return "POST method"
    if request.method == 'GET':
        if
        ct = datetime.datetime.now()




if __name__ == '__main__':
    app.run(debug=True)
