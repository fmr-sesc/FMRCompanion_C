# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math

# Connect to the Vehicle
print("Connecting")
connection_string = '192.168.0.1:14540'
vehicle = connect(connection_string, wait_ready=True)

