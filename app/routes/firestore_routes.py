# from flask import Blueprint, request, jsonify, make_response, abort
from os import environ
from app import db 
from ics import Calendar, Event
from flask import Blueprint, request, jsonify, make_response, abort
import requests
from datetime import datetime, timedelta, timezone, date, time
from dateutil import parser

# url = https://calendar.google.com/calendar/ical/v2u22eu9fu46ia671hf2lns0m8%40group.calendar.google.com/private-019bf05ca8425d86706d4dca2909a891/basic.ics"
# c = Calendar(requests.get(url).text)
# print(c)

collection = db.collection('users')
# doc = collection.document('AM4Y8EdoOQVeHZL7z11DNmvZ4LZ2')

firestore_bp = Blueprint('firestore', __name__, url_prefix="/firestore")

# # Get calendar link
# @calendar_bp.route("", methods=["GET"])
# def get_calendar():
#     request_body = request.get_json()
#     url = request_body["url"]
#     user = request_body["uid"]
#     doc = collection.document(user)
#     c = Calendar(requests.get(url).text)
    
#     calendar = {"calendar_details": str(c)}

#     # return jsonify(c)
#     return make_response(calendar, 200)


# Get user_info from firestore
@firestore_bp.route("", methods=["GET"])
def get_firestore_user_doc():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]
    doc = collection.document(user)
    res = doc.get().to_dict()

    return make_response(res, 200)

# Get events next (work on this after reminders)

# Get events today
# @firestore_bp.route("events/today", methods=["GET"])
# done in swift

# Post events today
@firestore_bp.route("events/today", methods=["POST"])
def post_firestore_events_today():
    request_body = request.get_json()

    user = request_body["uid"]
    url = collection.document(user).get().to_dict()["url"]

    c = Calendar(requests.get(url).text)

    now_with_micro_sec = datetime.now(timezone.utc)
    # date_time_now = now_with_micro_sec.isoformat(" ", "seconds")
    date_now = str(now_with_micro_sec.date())
    # time_now = date_time_now[11:]

    doc = collection.document(user).collection('user_info').document('events').collection('events_today')

    for event in c.events: 
        event_name = event.name
        start = str(event.begin)
        # end = str(event.end)
        event_date = start[0:10]
        event_time = start[11:16]
        if not event.location:
            location = "None"
        else:
            location = event.location
        description = event.description
        if ".com" in description:
            location = "virtual"

        if event_date == date_now:
            data = {
                "event_name": event_name,
                "start_time": event_date,
                "event_time": event_time,
                "location":location,
                "description":description
                }
            doc.document(event_name).set(data)

    # response = today_dict
    return make_response("posted", 200)

# Get events week (may have time for this)

# Post reminder preferences (called by setting reminder preferences) (returns dateInfo so Swift can set notifications)
@firestore_bp.route("reminders/preferences", methods=["POST"])
def post_reminder_preferences():
    # get uid from body
    request_body = request.get_json()
    user = request_body["uid"]

    # get url from firebase
    url = collection.document(user).get().to_dict()["url"]
    c = Calendar(requests.get(url).text)

    # save preferences
    every = int(request_body["every"])
    freq = int(request_body["freq"])
    # total = every * freq

    # get non-edited events and edit events with preferences  
    doc = collection.document(user).collection('user_info').document('events').collection('reminders')

    for event in c.events:
        # print(f'{doc.id} => {doc.to_dict()}')
        event_name = event.name
        start = str(event.begin)
        event_date = start[0:10]
        event_time = start[11:19]
        if not event.location:
            location = "None"
        else:
            location = event.location
        description = event.description
        if ".com" in description:
            location = "virtual"
        str_date_time = event_date + " " + event_time
        date_time = parser.parse(str_date_time)

        # i = 0
        for i in range(0,freq):
            time_change = timedelta(minutes=every)
            reminder = date_time - time_change
            # reminder_date = str(reminder)[0:10]
            reminder_name = f"{event_name}_Reminder{i+1}"
            reminder_day = str(reminder)[8:10]
            reminder_month = str(reminder)[5:7]
            reminder_year = str(reminder)[0:4]
            reminder_hour = str(reminder)[11:13]
            reminder_minute = str(reminder)[14:16]

            data = {
                "day": reminder_day,
                "month": reminder_month,
                "year": reminder_year,
                "hour": reminder_hour,
                "minute": reminder_minute,
                "event_name": event_name,
                "event_date": event_date,
                "event_time": event_time,
                "location": location,
                "description": description
                }
            # save reminders
            doc.document(reminder_name).set(data)

    return make_response("posted", 200)

# Get reminders (may have time for this)

# Posts events from calendar onto events doc and url into user <uid> doc
@firestore_bp.route("events", methods=["POST"])
def post_to_subcollection():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]
    address = {'url': url}

    c = Calendar(requests.get(url).text)

    events_dict = {}

    for event in c.events:
        event_name = event.name
        start = str(event.begin)
        end = str(event.end)
        event_date = start[0:10]
        event_time = start[11:]

        event_day = start[8:10]
        event_month = start[5:7]
        event_year = start[0:4]
        event_hour = start[11:13]
        event_minute = start[14:16]
        if not event.location:
            location = "None"
        else:
            location = event.location
        description = event.description
        if ".com" in description:
            location = "virtual"
        data = {
                "day": event_day,
                "month": event_month,
                "year": event_year,
                "hour": event_hour,
                "minute": event_minute,
                "location": location,
                "description": description
                }

        collection.document(user).collection('user_info').document(event_name).set(data)

    # doc = collection.document(user).collection('user_info').document('events')
    # doc.set(events_dict)
    collection.document(user).update(address)
    return make_response("posted", 200)
