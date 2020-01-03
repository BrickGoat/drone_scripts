from dronekit import connect, VehicleMode, LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
#Common attributes to check

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

vehicle = connectMyCopter()

#Version and attributes
vehicle.wait_ready('autopilot_version')
print('Autopilot version: %s' %vehicle.version)

#Does the firmware support the companion pc to set attitude
print('Supports set attitude from companion: %s' %vehicle.capabilities.set_attitude_target_local_ned)

#Read actual position
print('position: %s'%vehicle.location.global_relative_frame)

#Read actual attitude roll, pitch, yaw
print('Attitude: %s'%vehicle.attitude)

#Read the actial velocity (m/s)
print('Velocity: %s' %vehicle.velocity)

#When was last heartbeat received
print('Last heartbeat: %s'%vehicle.last_heartbeat)

#Is vehicle good to Arm
print('Armable: %s'%vehicle.is_armable)

#total groundspeed
print('Groundspeed: %s'%vehicle.groundspeed) #settable

#actual flight mode
print('Mode: %s'%vehicle.mode.name) #settable

#Is vehicle armed
print('Armed: %s'%vehicle.armed) #settable

#Is state estimation filter ok
print('EKF Ok: %s'%vehicle.ekf_ok)

vehicle.close()
