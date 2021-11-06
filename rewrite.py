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
                return None
        elif argType == 'int':
            try:
                return request.args.get(argName, type=int)
            except Exception as e:
                return None
        elif argType == 'flt':
            try:
                return request.args.get(argName, type=float)
            except Exception as e:
                return None
    else:
        try:
            return request.args.get(argName)
        except Exception as e:
            return None




@app.route("/praytimes/today", methods=['GET', 'POST'])
def praytimes():
    if request.method == 'POST':
        return "POST method"
    if request.method == 'GET':
        lat = ''
        long=''
        city = checkArg('city', 'str')
        if not city:
            lat, long = checkArg('lat', 'flt'), checkArg('long', 'flt')
            if not lat or not long:
                return "missing args city , lat or long"
            else:
                city = "no city"

        else:
            city = city
            geolocator = Nominatim(user_agent='prayer-times-rewrite')
            location = geolocator.geocode(city)
        juristic = checkArg('juristic', 'flt')
        if not juristic:
            juristic = 0 #Shafii , Maliki, Hambali
        else:
            juristic = juristic
        school = checkArg('school', 'flt')
        if not school:
            school = 4 # https://prayertimes.date/api/docs/today
        else:
            school = school
        ct = datetime.now()
        tf = TimezoneFinder()
        if city != "no city":
            timezone = float(pytz.timezone(tf.timezone_at(lng=location.longitude, lat=location.latitude)).utcoffset(
        datetime(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)).total_seconds() / 3600)
            pt = Prayer(PrayerConf(location.longitude, location.latitude, timezone, int(school), int(juristic)), date.today())
        elif lat and long:
            timezone = float(pytz.timezone(tf.timezone_at(lng=long, lat=lat)).utcoffset(
                datetime(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)).total_seconds() / 3600)
            pt  = Prayer(PrayerConf(long, lat, timezone, int(school),int(juristic), date.today()))

        prayer_times = {
                "Fajr": pt.fajr_time(),
                "Sherook": pt.sherook_time(),
                "Dohr": pt.dohr_time(),
                "Asr": pt.asr_time(),
                "Maghreb": pt.maghreb_time(),
                "Ishaa": pt.ishaa_time(),
                "Qiyam": pt.last_third_of_night()}
        #return render_template('prayers.html', prayers=prayer_times)
        return prayer_times





if __name__ == '__main__':
    app.run(debug=True)
