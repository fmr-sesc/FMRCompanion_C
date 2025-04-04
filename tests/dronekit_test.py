from dronekit import connect
import time

print("Connecting to drone")
vehicle = connect('udp:192.168.0.4:14540', wait_ready=True)
print("Drone Connected!")
while True:
    print(vehicle.battery)
    time.sleep(1)