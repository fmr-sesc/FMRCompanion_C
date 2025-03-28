#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys


async def run():
    drone = System()
    await drone.connect(system_address="udp://192.168.0.4:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    entries = await drone.log_files.get_entries()
    if entries:
        newest_entry = entries[-1]  # entries are sorted oldest → newest
        await download_log(drone, newest_entry)


async def download_log(drone, entry):
    date_without_colon = entry.date.replace(":", "-")
    filename = f"/home/FMRCompanion/ulog-{date_without_colon}.ulog"
    async for _ in drone.log_files.download_log_file(entry, filename):
        pass


if __name__ == "__main__":
    asyncio.run(run())
