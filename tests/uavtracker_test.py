import asyncio
from mavsdk import System

class UAVTracker:
    """Class to track the UAV's latitude and longitude in real-time."""
    def __init__(self, drone_address="udp://192.168.0.4:14540", logging_switch_channel=7):
        self.drone = System()
        self.latitude = 0.0
        self.longitude = 0.0
        self.drone_address = drone_address
        self.logging_switch_channel = logging_switch_channel
        self.logging_enabled = False

    async def run(self):
        """Main function to handle communication with UAV."""
        print("Waiting for connection to Drone")
        await self.drone.connect(system_address=self.drone_address)
        print("Drone Mavlink stream connected")

        # Keep all tasks running (Add new communication tasks here)
        await asyncio.gather(
            self.getPosition(),
            self.getLoggingSwitch()
        )

        while True:
            await asyncio.sleep(3)
    
    async def getPosition(self):
        """Continuously updates latitude and longitude from telemetry."""
        async for position in self.drone.telemetry.position():
            self.latitude = position.latitude_deg
            self.longitude = position.longitude_deg
    
    async def getLoggingSwitch(self):
        """Continuously checks RC input for switch position changes and updates corresponding flag."""
        async for rc_status in self.drone.telemetry.rc_status():
            channels = rc_status.channels
            print(channels)
            '''
            # Ensure channel is available
            if len(channels) > self.logging_switch_channel:
                # Read switch PWM value
                switch_value = channels[self.logging_switch_channel]

                # Detect switch position and set logging flag
                if switch_value > 1500 and not self.logging_enabled:
                    self.logging_enabled = True

                elif switch_value < 1500 and self.logging_enabled:
                    self.logging_enabled = False
            '''

drone =UAVTracker()
asyncio.run(drone.run())