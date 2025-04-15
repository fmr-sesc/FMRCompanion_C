from dronekit import connect
import time

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('udpout:192.168.0.4:14540')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
while True:
    print(f"Version: {vehicle.version}")
    print(f"Version: {vehicle.location.global_frame}")
    #Create a message listener using the decorator.
    @vehicle.on_message('GPS_INPUT')
    def listener(self, name, message):
        print(message)
    time.sleep(1)

# Once connected, use 'the_connection' to get and send messages