import time
import tca9548a
import smbus2

# init
# I2C Adresses of Multiplexer and Sensors
PCA95_ADDR = 0x71
HCL_ADDR = 0x78
# Initialise I2C Bus
bus = smbus2.SMBus(1)
# Initialise Multiplexer
tca_driver = tca9548a.TCA9548A(bus, PCA95_ADDR)
# Disable all I2C channels on multiplexer
tca_driver.set_control_register(0b00000000)
time.sleep(3)

while True:
    for i in range(4):
        # Enable channel
        tca_driver.set_channel(i, 1)
        data = bus.read_byte(HCL_ADDR)
        data <<= 8
        result = ((float(data) - 1638) / 5253) - 2.47
        print(f"Measured pressure at sensor {i+1} is {result:.2f} mbar")
        # Disable channel 4
        tca_driver.set_channel(i, 0)
    time.sleep(1)