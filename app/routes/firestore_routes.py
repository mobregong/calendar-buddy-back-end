# from flask import Blueprint, request, jsonify, make_response, abort
from os import environ
from app import db 
from ics import Calendar, Event
from flask import Blueprint, request, jsonify, make_response, abort
import requests

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


# Get events from firestore
@firestore_bp.route("", methods=["GET"])
def get_firestore():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]
    doc = collection.document(user)
    res = doc.get().to_dict()

    return make_response(res, 200)

# Test post to firestore
@firestore_bp.route("", methods=["PUT"])
def post_to_users():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]

    c = Calendar(requests.get(url).text)

    events_dict = {}
    i = 1
    for event in c.events:
        start = str(event.begin)
        end = str(event.end)
        if not event.location:
            location = "None"
        else:
            location = event.location
        description = event.description
        if ".com" in description:
            location = "virtual"
        events_dict[event.name] = [{"start_time": start},{"end_time": end},{"location":location},{"description":description}]
        i += 1

    doc = collection.document(user)
    res = doc.update(events_dict)
    return make_response("posted", 200)

@firestore_bp.route("events", methods=["PUT"])
def post_to_subcollection():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]

    c = Calendar(requests.get(url).text)

    events_dict = {}
    i = 1
    for event in c.events:
        start = str(event.begin)
        end = str(event.end)
        if not event.location:
            location = "None"
        else:
            location = event.location
        description = event.description
        if ".com" in description:
            location = "virtual"
        events_dict[event.name] = [{"start_time": start},{"end_time": end},{"location":location},{"description":description}]
        i += 1

    doc = collection.document(user).collection('user_info').document('events')
    res = doc.set(events_dict)
    return make_response("posted", 200)