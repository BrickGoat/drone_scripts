from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse

######FUNCTIONS#######

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

#####Main Excecutable######
vehicle = connectMyCopter()
print("Vehicle is connected")
vehicle.close()

