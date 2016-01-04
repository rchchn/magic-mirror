import json
import requests
import urllib
import geopy
import ast

# An example working waze call
#https://www.waze.com/RoutingManager/routingRequest?from=x%3A-73.8876574+y%3A40.7664011+bd%3Atrue&to=x%3A-73.7721035+y%3A40.7486434+bd%3Atrue&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=2
#from: http://stackoverflow.com/questions/19082391/php-json-decode-isnt-working-on-a-text-x-json-string-waze-route-calculation-api

class WazeLocationNotFoundException(Exception):
    pass

class Geocode(object):
    '''Returns address, latitude, and longitude of a given address (doesn't need to be fully formed, either!)'''
    def __init__(self, place):
        
        geolocator = geopy.geocoders.GoogleV3()
        address, (latitude,longitude) = geolocator.geocode(place)

        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        

class Waze(object):
    _BASE_URL = "http://waze.com/"
        

    def __routeData(self, fromLocation, toLocation, maxNumberOfRoutes):
        
        params = "from=x%3A"+str(fromLocation.longitude)+"+y%3A"+str(fromLocation.latitude)+"+bd%3Atrue&"+\
                 "to=x%3A"+str(toLocation.longitude)+"+y%3A"+str(toLocation.latitude)+"+bd%3Atrue&"+\
                 "returnJSON=true&"+\
                 "returnGeometries=false&"+\
                 "returnInstructions=true&"+\
                 "timeout=60000&"+\
                 "nPaths="+str(maxNumberOfRoutes)

        url = Waze._BASE_URL + "RoutingManager/routingRequest?"+params

        print url
        r = requests.get(url)
        json = r.json()
        #with open("temp.txt", "w+") as log:
        #    log.write(r.json())
        print type(json)
        return json

    def routes(self, source, target, maxNumberOfRoutes = 2):
        fromLocation = Geocode(source)
        toLocation = Geocode(target)
        #print fromLocation

        result = self.__routeData(fromLocation, toLocation, maxNumberOfRoutes)
        
        routes = []
        for route in result[u"alternatives"]:
            directions = []
            for direction in route[u"response"][u"results"]:
                directions.append({
                    "crossTime": direction[u"crossTime"],
                    "crossTimeWithoutRealTime": direction[u"crossTimeWithoutRealTime"],
                    "distance": direction[u"distance"],
                    "length": direction[u"length"],
                })
            routes.append(directions)

        return routes

if __name__ == "__main__":
    waze = Waze()
    print "Hello"
    
    routes = waze.routes("1447 southland vista court, atlanta", "1355 Bluegrass Lakes Parkway, 30004", 3)

    for index, route in enumerate(routes):
        print "Route %d" % index
        print "====================="
        print "Total length: %g mi" % ((sum([d["length"] for d in route]) / 1000.0) * 0.621371)
        print "Total time: %g mins" % (sum([d["crossTime"] for d in route]) / 60.0)
        print "Total time (w/o real time): %g mins" % (sum([d["crossTimeWithoutRealTime"] for d in route]) / 60.0)
        print
