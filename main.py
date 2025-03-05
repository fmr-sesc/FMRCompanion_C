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
sensorReadoutThread = threading.Thread(target=sensorReadout, args=(logger, bus), daemon=True)
updateDroneThread = threading.Thread(target=drone.run_in_thread, daemon=True)

sensorReadoutThread.start()
updateDroneThread.start()

# Setup dummy variable to detect True False transition in logging switch
previous_logging_state = False

dummy_enable = True
# Main loop (mainly used for logging and to keep threads running)
while True:
    # If logging switch changes from True to False create new csv
    if not previous_logging_state and dummy_enable:
        logger.create_csv
    # Write collected data to csv (sensor data already loaded to buffer)
    if dummy_enable:
        logger.log_data("Latitude", drone.latitude)
        logger.log_data("Longitude", drone.longitude)
        print(logger.data_buffer)
        logger.write_data_to_csv()
        
    previous_logging_state = drone.logging_enabled
    time.sleep(logger.sample_time)
