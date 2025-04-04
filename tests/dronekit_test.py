from dronekit import connect
import time

print("Connecting to drone")
vehicle = connect('0.0.0.0:14540', wait_ready=True)
print("Drone Connected!")
while True:
    print(vehicle.battery)
    time.sleep(1)