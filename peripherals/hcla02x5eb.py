import time
import peripherals.tca9548a as tca9548a
import smbus2

class HCLA02X5EB():
    def __init__(self, i2c_bus, address):
        """Init HCLA02X5EB sensor constants"""
        self.P_min = -2.5     # Minimum pressure readout
        self.Out_min = 1638   # Minimum count readout
        self.S = (27852 - 1638)/(2.5 - self.P_min)
        self.i2c_address = address
        self.i2c_bus = i2c_bus
    def get_pressure_reading(self):
        data = self.i2c_bus.read_byte(self.i2c_address)
        data <<= 8
        result = ((float(data) - self.Out_min) / self.S) + self.P_min
        return result