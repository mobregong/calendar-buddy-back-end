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
def get_firestore_user_doc():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]
    doc = collection.document(user)
    res = doc.get().to_dict()

    return make_response(res, 200)

# Get events next

# Get events today
@firestore_bp.route("events/today", methods=["GET"])
def get_firestore_events_today():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]

    doc = collection.document(user).collection('user_info').document('events')
    res = doc.get().to_dict()

    # # times = []
    # for event in res:
    #     print(event)
    # res["Event1"]

    return make_response(res["Event1"][0], 200)

# Get events week


# Post reminder preferences (called by setting reminder preferences) (returns dateInfo so Swift can set notifications)

# Get reminders (may have time for this)

# # Test post to firestore
# @firestore_bp.route("", methods=["PUT"])
# def post_to_users():
#     request_body = request.get_json()
#     url = request_body["url"]
#     user = request_body["uid"]

#     c = Calendar(requests.get(url).text)

#     events_dict = {}
#     i = 1
#     for event in c.events:
#         start = str(event.begin)
#         end = str(event.end)
#         if not event.location:
#             location = "None"
#         else:
#             location = event.location
#         description = event.description
#         if ".com" in description:
#             location = "virtual"
#         events_dict[event.name] = [{"start_time": start},{"end_time": end},{"location":location},{"description":description}]
#         i += 1

#     doc = collection.document(user)
#     res = doc.update(events_dict)
#     return make_response("posted", 200)

@firestore_bp.route("events", methods=["POST"])
def post_to_subcollection():
    request_body = request.get_json()
    url = request_body["url"]
    user = request_body["uid"]

    c = Calendar(requests.get(url).text)

    events_dict = {}

    for event in c.events:
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
        events_dict[event.name] = [{"day": event_day},{"month": event_month},{"year":event_year},{"hour":event_hour},{"minute":event_minute},{"start_time": start},{"end_time": end},{"location":location},{"description":description}]

    doc = collection.document(user).collection('user_info').document('events')
    res = doc.set(events_dict)
    return make_response("posted", 200)