import socket
import time
from builtins import object
from pymavlink.dialects.v20 import common as mavlink1
from pymavlink import  mavutil

time_since_start = 0

class fifo(object):
    def __init__(self):
        self.buf = []
    def write(self, data):
        self.buf += data
        return len(data)
    def read(self):
        return self.buf.pop(0)

# def check_msg_id(msg):
#     if():
#
#     elif():


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind(('',socket.htons(14451)))

# master = mavutil.mavlink_connection()

# gc = sockaddr_in()
# gc.sin_family = socket.AF_INET
# gc.sin_addr = "127.0.0.1"
# gc.sin_port = socket.htons(14550)

gcAddr = ("127.0.0.1", 14550)

sock.connect(gcAddr)

f = fifo()
mav = mavlink1.MAVLink(f)

while True:
    time_since_start += 100
    try:
        msg = mav.heartbeat_encode(mavlink1.MAV_TYPE_FIXED_WING, mavlink1.MAV_AUTOPILOT_GENERIC,
                                   mavlink1.MAV_MODE_MANUAL_ARMED, 0, mavlink1.MAV_STATE_ACTIVE)
        msg.pack(mav)
        sock.sendto(msg.get_msgbuf(), gcAddr)

        # msg = mav.attitude_encode(int(time_since_start), 1.12, 0.1, 2.71, 0., 0., 0.)
        # msg.pack(mav)
        # sock.sendto(msg.get_msgbuf(), gcAddr)

        msg = mav.param_value_encode(b'SYSID_THISMAV', 1., 0, 0, 0)
        msg.pack(mav)
        sock.sendto(msg.get_msgbuf(), gcAddr)

        data = sock.recvfrom(2048)
        print("Bytes received: %d\nDatagaram: %a" %(len(data[0]), data[0].decode("ISO-8859-1")))
        msg_ = mav.parse_char(data[0])
        if(msg_):
            print(f"Received packet: SYS: {msg_.get_srcSystem()}, "
                      f"COMP: {msg_.get_srcComponent()}, LEN: {len(msg_.get_msgbuf())}, "
                      f"MSG ID: {msg_.get_msgId()}")
        print()
        # if(msg_.get_msgId() == 1):

        time.sleep(1)

    except KeyboardInterrupt:
        sock.close()
        raise

    # except:
    #     print("Exit...")
    #     break

sock.close()