import gmaps

a = gmaps.Directions()
a=a.directions(origin="1447 Southland Vista Ct, 30329",
               destination="1355 Bluegrass Lakes Pkwy, 30004",
               alternatives=True,
               mode="driving")
overview = a[0]['overview_polyline']
warnings = a[0]['warnings']
bounds   = a[0]['bounds']
waypoints= a[0]['waypoint_order']
summary  = a[0]['summary']
legs     = a[0]['legs']


class GoogleAPI(object):
    def __init__(self):
        #This is a secret API key.  Don't share this! lol
        api_key = "AIzaSyD3Hym9XKu0O4KU3ZLrN5x4m2BKmITS8pg"

    def __docs__(self):
        return "http://python-gmaps.readthedocs.org/en/latest/"

