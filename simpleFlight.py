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

    
#####Main Excecutable######
vehicle = connectMyCopter()
print("Vehicle is connected")
armAndTakeoff(10)
vehicle.close()
