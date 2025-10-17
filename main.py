import smbus2
import threading
import time
from tools import Logger
from tools import UAVTracker
from tools import detect_USB_drive
from threads import sensorReadout

# Sample times (s)
sensorReadout_sample_time = 0.01
mavlink_sample_time = 0.01
logger_sample_time = 1

# Run init functions
usb_path = detect_USB_drive()
# Setup I2C port 1 of the RasPi
bus = smbus2.SMBus(1)
# Setup Logger
logger = Logger(usb_path=usb_path)
# Setup drone object for telemetry
drone = UAVTracker(gps_sample_time = 0.05, mav_send_sample_time = 0.02)

# Initialise threads
sensorReadoutThread = threading.Thread(target=sensorReadout, args=(logger, bus, drone, sensorReadout_sample_time), daemon=True)
updateDroneThread = threading.Thread(target=drone.run_in_thread, daemon=True)

# Start threads
sensorReadoutThread.start()
updateDroneThread.start()

# Setup dummy variable to detect True False transition in logging switch
previous_logging_state = False
dummy = True
# Main loop (mainly used for logging and to keep threads running)
while True:
    # On arm create new log file
    if not previous_logging_state and dummy:
        logger.create_csv(date_time=drone.system_time)
    # Write collected data to csv (sensor data already loaded to buffer)
    if dummy:
        logger.log_data("Latitude", drone.latitude)
        logger.log_data("Longitude", drone.longitude)
        logger.log_data("Altitude_MSL", drone.altitude_msl)
        logger.log_data("Altitude_AMSL", drone.altitude_amsl)
        logger.log_data("Airspeed", drone.airspeed)
        logger.log_data("Groundspeed", drone.groundspeed)
        logger.log_data("Heading", drone.heading)
        logger.log_data("Throttle", drone.throttle)
        logger.log_data("Climb", drone.climb)
        logger.write_data_to_csv()
        
    previous_logging_state = dummy
    time.sleep(logger.sample_time)