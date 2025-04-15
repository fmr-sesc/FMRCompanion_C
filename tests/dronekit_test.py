from dronekit import connect

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('0.0.0.0:14540', wait_ready=True)

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Once connected, use 'the_connection' to get and send messages