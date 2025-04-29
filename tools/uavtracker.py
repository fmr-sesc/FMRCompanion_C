import os
import time
import asyncio
from pymavlink import mavutil
from datetime import datetime
import math

# Set mavlink type to Mavlink 1
os.environ.pop('MAVLINK20', None)
# Set mavlink dialect to common
mavutil.set_dialect("common")

class UAVTracker:
    """Class to handle UAV mavlink communication"""
    def __init__(self, drone_address='udpout:192.168.0.4:14540', gps_sample_time = 0.05, mav_send_sample_time = 0.02):
        self.vehicle = None
        self.latitude = 0.0
        self.longitude = 0.0
        self.drone_address = drone_address
        self.logging_enabled = False
        self.gps_sample_time = gps_sample_time
        self.mav_send_sample_time = mav_send_sample_time
        self.system_time = None

    async def run(self):
        # Start connection over UDP
        self.vehicle = mavutil.mavlink_connection(self.drone_address, dialect="common")

        # Ping to initialise connection
        print("Ping drone and wait for connection")
        self.wait_conn()
        print("Drone Connected")

        # Wait for the first heartbeat to set the system and component ID of remote system for the link
        self.vehicle.wait_heartbeat()

        # Request SYSTEM_TIME message at 1 hz 
        self.request_message(2, 1)
        # Request GPS_RAW_INT at 20 hz
        self.request_message(24, 0.05)

        # Start asyncio coroutines
        await asyncio.gather(
            self.message_receiver(),
            self.message_dispatcher()
        )

    def wait_conn(self):
        """Sends a ping to stabilish the UDP communication and waits for a response"""
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
        return await loop.run_in_executor(None, lambda: self.vehicle.recv_match(type=msg_type, blocking=True))

    async def message_receiver(self):
        '''Function to watch incomming mavlink traffic und update parameters corresponding to the messages'''
        while True:
            msg = await self.get_mavlink_msg(msg_type=None)  # Receive any message
            if not msg:
                continue

            msg_type = msg.get_type()

            # Update parameters based on message type
            if msg_type == 'SYSTEM_TIME':
                self.system_time = datetime.utcfromtimestamp(msg.time_unix_usec / 1e6)
                print(f"[DateTime] {self.system_time}")

            elif msg_type == 'GPS_RAW_INT':
                self.latitude = msg.lat
                self.longitude = msg.lon
                print(self.latitude, self.longitude)

            elif msg_type == 'HEARTBEAT':
                self.logging_enabled = (msg.system_status == 4)
                print(f"[Armed] {self.logging_enabled}")

            await asyncio.sleep(0.001)  # Yield control

    async def message_dispatcher(self):
        x = 0
        while True:
            self.vehicle.mav.fmr_sensors_send(
            sens_1=math.sin(x),
            sens_2=2.71,
            sens_3=2.71,
            sens_4=2.71,
            sens_5=2.71
            )
            x = x + 0.1
            await asyncio.sleep(self.mav_send_sample_time)