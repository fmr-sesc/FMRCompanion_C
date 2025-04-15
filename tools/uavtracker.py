import asyncio
import os
from mavsdk import System
from dronekit import connect

class UAVTracker:
    """Class to track the UAV's latitude and longitude in real-time."""
    def __init__(self, drone_address="udp://192.168.0.4:14540", usb_path = None):
        self.drone = System()
        self.latitude = 0.0
        self.longitude = 0.0
        self.drone_address = drone_address
        self.logging_enabled = False
        self.usb_path = usb_path

    async def run(self):
        """Main function to handle communication with UAV."""
        print("Waiting for MAVSDK connection to Drone")
        await self.drone.connect(system_address=self.drone_address)
        print("MAVHSDK drone Mavlink stream connected")
        print("Waiting for UDP connection to Drone")
        vehicle = connect('udpout:192.168.0.4:14540')
        print("Dronekit connection stablished")

        
        # Trigger to download log
        self._download_trigger = asyncio.Event()

        # Keep all tasks running (Add new communication tasks here)
        await asyncio.gather(
            self.getPosition(),
            self.getLoggingSwitch(),
            self.downloadPX4LogLoop(),
            self.dronekitPosition(vehicle=vehicle)
        )
    
    async def getPosition(self):
        """Continuously updates latitude and longitude from telemetry."""
        async for position in self.drone.telemetry.position():
            self.latitude = position.latitude_deg
            self.longitude = position.longitude_deg
    
    async def dronekitPosition(self, vehicle):
        """Continuously updates latitude and longitude from telemetry."""
        print(vehicle.vehicle.location.global_frame)
        await asyncio.sleep(1)
    
    async def getLoggingSwitch(self):
        """Continuously checks arm status and enables logging flag when armed."""
        async for armed in self.drone.telemetry.armed():
            self.logging_enabled = armed

    def triggerPX4LogDownload(self):
        """Call this to trigger download of log."""
        self._download_trigger.set()
    
    async def downloadPX4LogLoop(self):
        '''Function that waits for the logdownload trigger and if activated starts log download'''
        while True:
            await self._download_trigger.wait()
            await self.downloadPX4Log()
            self._download_trigger.clear()

    async def downloadPX4Log(self):
        '''Function that downloads the newest loge entry by datetime lable of PX4 log'''
        entries = await self.drone.log_files.get_entries()
        if entries:
            newest_entry = entries[-1]
            date = newest_entry.date.replace(":", "-")
            filename = f"PX4_log_{date}.ulog"
            file_path = os.path.join(self.usb_path, filename)
            async for _ in self.drone.log_files.download_log_file(newest_entry, file_path):
                pass

    def run_in_thread(self):
        """Setup seperate event loop to run in thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())