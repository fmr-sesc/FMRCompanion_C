from tools import UAVTracker
import time
import threading

drone = UAVTracker()

updateDroneThread = threading.Thread(target=drone.run, daemon=True)
updateDroneThread.start()

while True:
    print(drone.latitude)
    print(drone.longitude)
    print(drone.logging_enabled)