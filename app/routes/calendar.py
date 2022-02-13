# from flask import Blueprint, request, jsonify, make_response, abort
# from app import db
from ics import Calendar, Event
from flask import Blueprint, request, jsonify, make_response, abort
import requests

# url = https://calendar.google.com/calendar/ical/v2u22eu9fu46ia671hf2lns0m8%40group.calendar.google.com/private-019bf05ca8425d86706d4dca2909a891/basic.ics"
# c = Calendar(requests.get(url).text)

# print(c)

calendar_bp = Blueprint('calendar', __name__, url_prefix="/calendars")

@calendar_bp.route("", methods=["GET"])
def get_boards():
    request_body = request.get_json()
    url = request_body["url"]
    c = Calendar(requests.get(url).text)
    
    calendar = {"calendar_details": str(c)}


    # return jsonify(c)
    return make_response(calendar, 200)
