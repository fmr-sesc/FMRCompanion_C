import smbus2

I2C_BUS = 1     # Use I2C bus 1 on pi
PC95_ADDR = 0x71# Adress of PCA95 multiplexer
HCL_ADDR = 0x78


bus = smbus2.SMBus(I2C_BUS)

def select_channel(channel):
    assert 0 <= channel <= 7
    bus.write_byte(PC95_ADDR, 1 << channel)
    bus.close()

def read_channel():
    value = bus.read_byte(HCL_ADDR)
    value <<= 8
    result = ((float(value)-1638)/5253) - 2.47
    bus.close()
    return result
    

while True:
    for i in range(4):
        select_channel(i)
        pressure = read_channel()
        print(f"Sensor id: {i}")
        print(i)
        print(f"Pressure:")
        print(pressure)