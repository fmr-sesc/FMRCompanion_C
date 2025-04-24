import time
from pymavlink import mavutil

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
    master.mav.fmr_sensors_send(1, 2, 3, 4, 5)
    time.sleep(0.0001)