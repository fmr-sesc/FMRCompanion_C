import os
os.environ['MAVLINK_DIALECT'] = 'common'
os.environ.pop('MAVLINK20', None)
import time
from pymavlink import mavutil

mavutil.set_dialect("common")
print(mavutil.mavlink.__name__)
def wait_conn():
    """
    Sends a ping to stabilish the UDP communication and awaits for a response
    """
    msg = None
    while not msg:
        master.mav.ping_send(
            int(time.time() * 1e6), # Unix time in microseconds
            0, # Ping number
            0, # Request ping of all systems
            0 # Request ping of all components
        )
        msg = master.recv_match()
        time.sleep(0.5)

# Start connection over UDP
master = mavutil.mavlink_connection('udpout:192.168.0.4:14540', dialect="common")

# Ping to initialise connection
print("Waiting for connection")
wait_conn()
print("Drone Connected")

while True:
    try:
        print(master.recv_match(type='ATTITUDE').to_dict())
        #print(master.recv_match('LOCAL_POSITION_NED').to_dict())
    except:
        pass
    print(dir(master.mav))
    # Create and send your custom message
    msg = master.mav.fmr_sensors_encode(
        sens_1=3.14,
        sens_2=2.71,
        sens_3=2.71,
        sens_4=2.71,
        sens_5=2.71
    )
    master.mav.send(msg)
    time.sleep(0.01)