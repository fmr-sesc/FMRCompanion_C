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

        # Ping to initialise connection
        print("Ping drone and wait for connection")
        self.wait_conn()
        print("Drone Connected")


        while True:
                try:
                    print(self.vehicle.messages['GPS_RAW_INT'].alt)
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