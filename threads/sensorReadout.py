from peripherals import HCLA02X5EB, TCA9548A
import time

def sensorReadout(logger, bus, drone, sample_time=0.01, HCLA02X5EB_ADDR=0x78, TCA9548A_ADDR_1=0x72, TCA9548A_ADDR_2=0x73):
    '''Function to readout all sensor data and automatically write the data to the logger buffer'''
    # Setup pressure sensor
    HCL_sens = HCLA02X5EB(bus, HCLA02X5EB_ADDR)
    # Setup Multiplexer
    TCA1 = TCA9548A(bus, TCA9548A_ADDR_1)
    TCA2 = TCA9548A(bus, TCA9548A_ADDR_2)
    # Disable all I2C channels on multiplexer
    TCA1.set_control_register(0b00000000)
    TCA2.set_control_register(0b00000000)

    # Main Loop
    while True:
        # Readout and log Pressure sensors 1 - 3
        for i in range(3):
            # Enable channel
            TCA1.set_channel(i, 1)
            pressure = HCL_sens.get_pressure_reading()
            logger.log_data(f"Pressure Sensor {i+1}", pressure)
            drone.mav_sensor_values[i] = pressure
            #print(f"Written pressure at sensor {i+1} is {drone.mav_sensor_values[i]:.2f} mbar")
            
            # Disable channel
            TCA1.set_channel(i, 0)
    
        # Readout and log Pressure sensors 4 - 6
        for i in range(3):
            # Enable channel
            TCA2.set_channel(i, 1)
            pressure = HCL_sens.get_pressure_reading()
            logger.log_data(f"Pressure Sensor {i+4}", pressure)
            drone.mav_sensor_values[i+3] = pressure
            #print(f"Written pressure at sensor {i+4} is {drone.mav_sensor_values[i]:.2f} mbar")
            
            # Disable channel
            TCA2.set_channel(i, 0)
    
    # Wait before next sample
    time.sleep(sample_time)