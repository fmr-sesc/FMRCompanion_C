from peripherals import HCLA02X5EB, TCA9548A
import time

def sensorReadout(logger, bus, drone, sample_time=0.01, HCLA02X5EB_ADDR=0x78, TCA9548A_ADDR=0x72):
    '''Function to readout all sensor data and automatically write the data to the logger buffer'''
    # Setup pressure sensor
    HCL_sens = HCLA02X5EB(bus, HCLA02X5EB_ADDR)
    # Setup Multiplexer
    TCA_multiplex = TCA9548A(bus, TCA9548A_ADDR=0x72)
    # Disable all I2C channels on multiplexer
    TCA_multiplex.set_control_register(0b00000000)

    # Main Loop
    while True:
        # Readout and log Pressure sensors
        for i in range(3):
            # Enable channel
            TCA_multiplex.set_channel(i, 1)
            pressure = HCL_sens.get_pressure_reading()
            logger.log_data(f"Pressure Sensor {i+1}", pressure)
            drone.mav_sensor_values[i] = pressure
            print(f"Written pressure at sensor {i+1} is {drone.mav_sensor_values[i]:.2f} mbar")
            # Disable channel
            TCA_multiplex.set_channel(i, 0)
        time.sleep(sample_time)