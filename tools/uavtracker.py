import os
import time
import asyncio
from pymavlink import mavutil
from datetime import datetime

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
        self.system_time = None

    async def run(self):
        # Start connection over UDP
        self.vehicle = mavutil.mavlink_connection(self.drone_address, dialect="common")

        # Ping to initialise connection
        print("Ping drone and wait for connection")
        self.wait_conn()
        print("Drone Connected")

        # Wait for the first heartbeat to set the system and component ID of remote system for the link
        print("Waiting for heartbeat")
        self.vehicle.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.vehicle.target_system, self.vehicle.target_component))

        # Request SYSTEM_TIME message at 1 hz 
        self.request_message(2, 1)
        # Request GPS_RAW_INT at 50 hz
        self.request_message(24, 0.02)

        await asyncio.gather(
            self.get_system_time()
            #self.get_gps_position()
        )
        
        '''
        # Main loop
        while True:
            msg = self.vehicle.recv_match(blocking=True, timeout=2)
            if not msg:
                continue

            if msg.get_type() == 'SYSTEM_TIME':
                print("SYSTEM_TIME:", msg.time_unix_usec)
            elif msg.get_type() == 'GPS_RAW_INT':
                print(f"GPS lat: {msg.lat}, lon: {msg.lon}")
            elif msg.get_type() == 'ATTITUDE':
                print(f"Roll: {msg.roll}, Pitch: {msg.pitch}")
        '''

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

    def request_message(self, message_id, message_sample_time):
        '''
        Function to request a specific mavlink message from the FC
        message_id: Mavlink message id defined in pymavlink/dialects/v10/common.py
        message_sample_time: Frequency at which the message has to be send in seconds
        '''
        # Define command_long_encode message to send MAV_CMD_SET_MESSAGE_INTERVAL command
        # param1: MAVLINK_MSG_ID_BATTERY_STATUS (message to stream)
        # param2: 1000000 (Stream interval in microseconds)
        message = self.vehicle.mav.command_long_encode(
                self.vehicle.target_system,  # Target system ID
                self.vehicle.target_component,  # Target component ID
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
                0,  # Confirmation
                message_id,  # param1: Message ID to be streamed
                message_sample_time * 1e6, # param2: Interval in microseconds
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
            print(f"Command accepted for message: {message_id} with sample time: {message_sample_time}")
        else:
            print(f"Command failed for message: {message_id} with sample time: {message_sample_time}")

    def run_in_thread(self):
        """Setup seperate event loop to run in thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())

    async def get_mavlink_msg(self, msg_type):
        '''Asyncio executor for recieving mavlink messages'''
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.vehicle.recv_match(type=msg_type, blocking=True, timeout=2))
    
    async def get_system_time(self):
        '''Coroutine to get system time from UAV'''
        while True:
            msg = await self.get_mavlink_msg(msg_type='SYSTEM_TIME')
            if msg:
                self.system_time = datetime.utcfromtimestamp(msg.time_unix_usec / 1e6)
                print(f"[DateTime] {self.system_time}")
            await asyncio.sleep(0)  # Yield control to other coroutines

    async def get_gps_position(self):
        '''Coroutine to get latitude and longitude of UAV'''
        while True:
            msg = await self.get_mavlink_msg(msg_type='GPS_RAW_INT')
            if msg:
                self.latitude = msg.lat
                self.longitude = msg.lon
                print(self.latitude)
                print(self.longitude)
            await asyncio.sleep(0)