from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
######FUNCTIONS#######
#create vehicle object with arg of drone host on port 5760 or 14550
def connectMyCopter():
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect', '-c', help="Vehicle connection string. See https://dronekit-python.readthedocs.io/en/latest/guide/connecting_vehicle.html for details.", dest="connection_string")
    args = parser.parse_args()

    connection_string = args.connect
    #start simulation if no args
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    #Serial port connection
    #vehicle = connect(connection_string,wait_ready=True, baud=57600)
    #TCP UDP
    vehicle = connect(connection_string,wait_ready=True)
    return vehicle

#preform preflight checks and fly to 95% of target height
def armAndTakeoff(targetHeight):
    #wait for vehicle to become armable
    while vehicle.is_armable!=True:
        print("Waiting for vehicle to become armable")
        time.sleep(1)
    print("Vehicle now armable.")

    #wait for vehicle to enter guided flight mode
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode!="GUIDED":
        print("Waiting for vehicle to enter GUIDED flight mode")
        time.sleep(1)
    print("Vehicle now in GUIDED MODE.")

    #wait for vehicle to arm
    vehicle.armed = True
    while vehicle.armed == False:
        print("Waiting for vehicle to become armed")
        time.sleep(1)
    print("CAUTION: PROPS SPINNING")

    #takeoff to a height within 95% of target
    vehicle.simple_takeoff(targetHeight)
    while True:
        print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= .95*targetHeight:
            break
        time.sleep(1)
    print("Target altitude of %d has been reached"%targetHeight)
    return None

#get distance from waypoint
def getDistanceM(targetLocation, currentLocation):
    dLat = targetLocation.lat - currentLocation.lat
    dLon = targetLocation.lon - currentLocation.lon
    #Less accurate the further the points are away
    dist = math.sqrt((dLon*dLon) + (dLat*dLat))*1.113195e5
    return dist

#travel to specified waypoint
def goTo(targetLocation):
    #fly to target and get distance in meters
    distanceToTarget = getDistanceM(targetLocation, vehicle.location.global_relative_frame)
    if distanceToTarget <= 1:
        print("Too close to waypoint")
        return None
    vehicle.simple_goto(targetLocation)
    
    #fly to a distance within 1% of target
    while vehicle.mode.name == "GUIDED":
        currentDistance = getDistanceM(targetLocation, vehicle.location.global_relative_frame)
        if currentDistance < distanceToTarget * .01:
            print("Reached target waypoint")
            time.sleep(2)
            break
        time.sleep(1)
    return None

#Land immediately
def land():
    vehicle.mode = VehicleMode("LAND")
    while vehicle.mode != 'LAND':
        print("Waiting for drone to enter LAND mode")
        time.sleep(1)
    print("Landing Drone")
    while vehicle.location.global_relative_frame.alt > .5:
        print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
        time.sleep(2)
    print("Vehicle has landed")
    return None

#####Main Excecutable######
vehicle = connectMyCopter()
print("Vehicle is connected")
armAndTakeoff(10)
waypoint = LocationGlobalRelative(34.713772,-77.2163,10)
print("Flying to waypoint")
goTo(waypoint)
land()
while True:
    time.sleep(1)
vehicle.close()

