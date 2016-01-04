import json
import requests
import urllib
import geopy
import ast
import env

# Some of the ideas from this code were taken and udpated from this guy:  https://github.com/dferrante/waze.  Thanks!  A great start!

# An example working waze call
#https://www.waze.com/RoutingManager/routingRequest?from=x%3A-73.8876574+y%3A40.7664011+bd%3Atrue&to=x%3A-73.7721035+y%3A40.7486434+bd%3Atrue&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=2
#from: http://stackoverflow.com/questions/19082391/php-json-decode-isnt-working-on-a-text-x-json-string-waze-route-calculation-api


class WazeLocationNotFoundException(Exception):
    pass

class Geocode(object):
    '''Returns address, latitude, and longitude of a given address (doesn't need to be fully formed, either!)'''
    def __init__(self, place):
        '''Uses Google V3.0 Engine to translate any non-fully-formed address to a fully formed address and let/long coordinate'''
        geolocator = geopy.geocoders.GoogleV3()
        address, (latitude,longitude) = geolocator.geocode(place)

        #set these global variables so that the program can use class.address, class.latitude, etc. to call the data
        self.address = address #The fully formed address
        self.latitude = latitude #The latitude coord
        self.longitude = longitude #the longitude coord

        
        

class WazeAPI(object):
    _BASE_URL_ = "http://waze.com/"
    
    
    def __routeData(self, fromLocation, toLocation, maxNumberOfRoutes):
        
        params = "from=x%3A"+str(fromLocation.longitude)+"+y%3A"+str(fromLocation.latitude)+"+bd%3Atrue&"+\
                 "to=x%3A"+str(toLocation.longitude)+"+y%3A"+str(toLocation.latitude)+"+bd%3Atrue&"+\
                 "returnJSON=true&"+\
                 "returnGeometries=false&"+\
                 "returnInstructions=true&"+\
                 "timeout=60000&"+\
                 "nPaths="+str(maxNumberOfRoutes)
        #Form a URL call to the waze servers
        url = WazeAPI._BASE_URL_ + "RoutingManager/routingRequest?" + params

        env.log.info(url)
        r = requests.get(url)
        json = r.json()
        #with open("temp.txt", "w+") as log:
        #    log.write(r.json())
        
        return json

    def GetRouteData(self, source, destination, maxNumberOfRoutes = 2):
        #Geocode the source and destination address to get latitude and longitude data
        fromLocation = Geocode(source)
        toLocation = Geocode(destination)

        #Retrieve route data from Waze
        raw_data = self.__routeData(fromLocation, toLocation, maxNumberOfRoutes)

        #Parse out only the important stuff: cross times, distances, and lengths
        routes = []
        for route in raw_data[u"alternatives"]:
            directions = []
            for direction in route[u"response"][u"results"]:
                directions.append({
                    "crossTime": direction[u"crossTime"],
                    "crossTimeWithoutRealTime": direction[u"crossTimeWithoutRealTime"],
                    "distance": direction[u"distance"],
                    "length": direction[u"length"],
                })
            routes.append(directions)
        
        return raw_data, routes
