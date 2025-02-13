"""
Tca9548a basic usage example
"""
import time

import tca9548a
import smbus2


def example():
    # init
    i2c_address = 0x71
    tca_driver = tca9548a.TCA9548A(i2c_address)

    # disable all i2c channels
    tca_driver.set_control_register(0b00000000)  # each bit controls a channel

    # enable channel 4
    tca_driver.set_channel(2, 1)

    # read state of channel 4
    ch4 = tca_driver.get_channel(2)
    print("Channel 4 is set to {}".format(ch4))

    # disable channel 4
    tca_driver.set_channel(2, 0)
# init
#i2c_address = 0x70
#tca_driver = tca9548a.TCA9548A(i2c_address)
bus = smbus2.SMBus(1)
time.sleep(1)

while True:
    example()
    time.sleep(1)
    data = bus.read_byte(0x78)
    data <<= data
    result = ((float(data) - 1638) / 5253) - 2.47
    print(result)
    time.sleep(1)