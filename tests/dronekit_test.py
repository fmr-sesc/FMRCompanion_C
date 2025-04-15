from dronekit import connect

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('0.0.0.0:14540')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
print(f"Heartbeat from system (system %u component %u) {vehicle.version}")

# Once connected, use 'the_connection' to get and send messages