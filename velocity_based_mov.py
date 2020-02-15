from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil
######FUNCTIONS#######
#create vehicle object with arg of drone host on port 5760 or 14550
def connectMyCopter():
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    args = parser.parse_args()
    connection_string = args.connect
    #use simulated drone if no args specified
    vehicle = connect(connection_string, wait_ready=True)
    return vehicle
'''    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()
        vehicle = connect(connection_string, wait_ready=True)
    else:
         vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)
'''

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

#Send MavLink velocity command for 1 second with +x being the front of the drone
def send_local_velocity(vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
            0b0000111111000111, #Bitmask for only velocities
            0, 0, 0,    #position
            vx, vy, vz, #velocity(NED+)
            0, 0, 0,    #Acceleration
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

#Send MavLink velocity command for 1 second with +x being the true North of Earth
def send_global_velocity(vx,vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,      #Time to boot in ms
            0, 0,   #Target system, Target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED, #Frame
            0b0000111111000111, #bitmask for velocity
            0, 0, 0,#position
            vx, vy, vz,
            0, 0, 0,#acceleration
            0, 0)   #Yaw, Yaw rate
    vehicle.send_mavlink(msg)
    vehicle.flush()


#####Main Excecutable######
vehicle = connectMyCopter()
print("Vehicle is connected")
armAndTakeoff(10)

count = 0
while count < 5:
    send_local_velocity(1, 0, 0)
    time.sleep(1)
    print("Moving North relative to drone")
    count = count + 1

time.sleep(2)

count = 0
while count < 5:
    send_local_velocity(-1, 0, 0)
    time.sleep(1)
    print("Moving South relative to drone")
    count = count + 1

time.sleep(2)

count = 0
while count < 5:
    send_local_velocity(0, 1, 0)
    time.sleep(1)
    print("Moving East relative to drone")
    count = count + 1

time.sleep(2)

count = 0
while count < 5:
    send_local_velocity(0, -1, 0)
    time.sleep(1)
    print("Moving West relative to drone")
    count = count + 1

time.sleep(2)

land()

time.sleep(30)

vehicle.close()
