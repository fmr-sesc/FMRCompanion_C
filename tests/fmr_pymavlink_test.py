from pymavlink.dialects.v10 import common as mavlink1
from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udpout:192.168.0.4:14540', dialect="common")