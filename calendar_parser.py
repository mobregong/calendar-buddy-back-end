from ics import Calendar
import requests

# url = "https://urlab.be/events/urlab.ics"
url = "https://calendar.google.com/calendar/ical/v2u22eu9fu46ia671hf2lns0m8%40group.calendar.google.com/private-019bf05ca8425d86706d4dca2909a891/basic.ics"
c = Calendar(requests.get(url).text)
e = list(c.timeline)[1]

# print(c)
# print(c.events)
print(e.name)
print(e.end)
# print("Event '{}' started {}".format(e.name, e.begin.humanize()))