from peripherals import HCLA02X5EB, TCA9548A
import smbus2
import time
from tools import Logger

# Constants
HCLA02X5EB_ADDR = 0x78
TCA9548A_ADDR = 0x71

# Setup I2C port 1
bus = smbus2.SMBus(1)
# Setup pressure sensor
HCL_sens = HCLA02X5EB(bus, HCLA02X5EB_ADDR)
# Setup Multiplexer
TCA_multiplex = TCA9548A(bus, TCA9548A_ADDR)
# Disable all I2C channels on multiplexer

TCA_multiplex.set_control_register(0b00000000)
# Setup Logger
logger = Logger()
logger.create_csv()


while True:
    for i in range(4):
        # Enable channel
        TCA_multiplex.set_channel(i, 1)
        pressure = HCL_sens.get_pressure_reading()
        logger.log_data(f"Pressure Sensor {i+1}", pressure)
        print(f"Measured pressure at sensor {i+1} is {pressure:.2f} mbar")
        # Disable channel
        TCA_multiplex.set_channel(i, 0)
    logger.write_data_to_csv()
    time.sleep(1)
