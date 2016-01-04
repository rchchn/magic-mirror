import api.waze_api as WazeAPI
import env #Application Environment Setup



print "Set up logging environment: complete"

START_ADDRESS = "1447 Southland Vista Court, 30306"
END_ADDRESS = "1355 Bluegrass Lakes Parkway, 30004"

if __name__ == "__main__":
    waze = WazeAPI.WazeAPI()
    env.log.info("Executing route")
    result, routes = waze.GetRouteData(START_ADDRESS, END_ADDRESS, maxNumberOfRoutes=3)
    

    for index, route in enumerate(routes):
        print "Route %d" % index
        print "====================="
        print "Total length: %g mi" % ((sum([d["length"] for d in route]) / 1000.0) * 0.621371)
        print "Total time: %g mins" % (sum([d["crossTime"] for d in route]) / 60.0)
        print "Total time (w/o real time): %g mins" % (sum([d["crossTimeWithoutRealTime"] for d in route]) / 60.0)
        print
