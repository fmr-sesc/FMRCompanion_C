from tools import UAVTracker_DK
import time
import threading

drone = UAVTracker_DK()

updateDroneThread = threading.Thread(target=drone.run, daemon=True)
updateDroneThread.start()

while True:
    #print(UAVTracker_DK.latitude)
    #print(UAVTracker_DK.longitude)
    #print(UAVTracker_DK.logging_enabled)
    time.sleep(0.001)