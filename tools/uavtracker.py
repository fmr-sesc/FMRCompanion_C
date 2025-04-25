import os
import time
from pymavlink import mavutil

# Set mavlink type to Mavlink 1
os.environ.pop('MAVLINK20', None)
# Set mavlink dialect to common
mavutil.set_dialect("common")

class UAVTracker:
    """Class to handle UAV mavlink communication"""
    def __init__(self, drone_address='udpout:192.168.0.4:14540', usb_path = None, sample_time = 0.1):
        self.vehicle = None
        self.latitude = 0.0
        self.longitude = 0.0
        self.drone_address = drone_address
        self.logging_enabled = False
        self.usb_path = usb_path
        self.sample_time = sample_time

    def run(self):
        # Start connection over UDP
        self.vehicle = mavutil.mavlink_connection('udpout:192.168.0.4:14540', dialect="common")

        print(self.vehicle.target_system)
        print(self.vehicle.target_component)

        # Ping to initialise connection
        print("Ping drone and wait for connection")
        self.wait_conn()
        print("Drone Connected")

        # Wait for the first heartbeat to set the system and component ID of remote system for the link
        print("Waiting for heartbeat")
        self.vehicle.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.vehicle.target_system, self.vehicle.target_component))


        # Define command_long_encode message to send MAV_CMD_SET_MESSAGE_INTERVAL command
        # param1: MAVLINK_MSG_ID_BATTERY_STATUS (message to stream)
        # param2: 1000000 (Stream interval in microseconds)
        message = self.vehicle.mav.command_long_encode(
                self.vehicle.target_system,  # Target system ID
                self.vehicle.target_component,  # Target component ID
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
                0,  # Confirmation
                2,  # param1: Message ID to be streamed
                10000, # param2: Interval in microseconds
                0,       # param3 (unused)
                0,       # param4 (unused)
                0,       # param5 (unused)
                0,       # param5 (unused)
                0        # param6 (unused)
                )

        # Send the COMMAND_LONG
        self.vehicle.mav.send(message)

        # Wait for a response (blocking) to the MAV_CMD_SET_MESSAGE_INTERVAL command and print result
        response = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True)
        if response and response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL and response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print("Command accepted")
        else:
            print("Command failed")


        while True:
                try:
                    print(self.vehicle.recv_match('SYSTEM_TIME'))
                    print(self.vehicle.recv_match('ATTITUDE'))
                    #print(self.vehicle.recv_match('GPS_RAW_INT').lat)
                    #print(self.vehicle.recv_match('GPS_RAW_INT').lon)
                except:
                    pass
                time.sleep(self.sample_time)

    def wait_conn(self):
        """Sends a ping to stabilish the UDP communication and awaits for a response"""
        msg = None
        while not msg:
            self.vehicle.mav.ping_send(
                int(time.time() * 1e6), # Unix time in microseconds
                0, # Ping number
                0, # Request ping of all systems
                0 # Request ping of all components
            )
            msg = self.vehicle.recv_match()
            time.sleep(0.5)