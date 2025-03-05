import smbus2
import threading
import time
import asyncio
from tools import Logger
from tools import UAVTracker
from threads import sensorReadout

# Setup I2C port 1 of the RasPi
bus = smbus2.SMBus(1)
# Setup Logger
logger = Logger()
# Setup drone object for telemetry
drone = UAVTracker()

# Initialise sensor Thread
sensorReadoutThread = threading.Thread(target=sensorReadout(logger, bus), daemon=True)

# Initialise asyncio drone Thread
def run_uav_tracker_in_thread():
    drone = UAVTracker()
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)     # Set the new event loop
    loop.run_until_complete(drone.run())  # Run the run() method

updateDroneThread = threading.Thread(target=run_uav_tracker_in_thread, daemon=True)

sensorReadoutThread.start()
updateDroneThread.start()

# Setup dummy variable to detect True False transition in logging switch
previous_logging_state = False

# Main loop (mainly used for logging and to keep threads running)
while True:
    # If logging switch changes from True to False create new csv
    if not previous_logging_state and drone.logging_enabled:
        logger.create_csv
    # Write collected data to csv (sensor data already loaded to buffer)
    if drone.logging_enabled:
        logger.log_data("Latitude", drone.latitude)
        logger.log_data("Longitude", drone.longitude)
        logger.write_data_to_csv()
        
    previous_logging_state = drone.logging_enabled
    time.sleep(logger.sample_time)
