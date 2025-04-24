import sys
sys.path.append("/home/FMRCompanion/FMR-mavlink/pymavlink")

from pymavlink.dialects.v10 import common as mavlink1
from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udpout:192.168.0.4:14540', dialect="pymavlink.dialects.v10.common")

the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
