# import socket UNCOMMENT JIKA INGIN MENGGUNAKAN SOCKET
import time
from builtins import object

from pymavlink import mavutil
from pymavlink.dialects.v20 import common as mavlink1

time_since_start = 0

class fifo(object):
    def __init__(self):
        self.buf = []
    def write(self, data):
        self.buf += data
        return len(data)
    def read(self):
        return self.buf.pop(0)

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)

parser.add_argument("--baudrate", dest="baudrate", type=int,
                        help="serial port baud rate", default=57600)
parser.add_argument("--com", dest="comport", type=str,
                        help="serial com port", default=None)
parser.add_argument("--udpin", dest="from_gcs", type=str,
                    help="membuka port untuk menerima pesan"
                         "dari GCS. (True / False)", default=False)

args = parser.parse_args()

if(args.from_gcs == "False" or args.from_gcs == "FALSE"  or args.from_gcs == "false" ):
    from_gcs = False
elif(args.from_gcs == "True" or args.from_gcs == "TRUE"  or args.from_gcs == "true" ):
    from_gcs = True

print("Selamat datang di uji coba pesan mavlink!")
time.sleep(1)
print("Program ini akan menguji coba pengiriman pesan mavlink dengan alur:")
print("\nFC->Com Port->Program ini->UDP->GCS\n")
time.sleep(1)
print("GCS yang digunakan untuk saat ini adalah QGroundControl.")

if (args.comport == None):
    serPort = "COM" + input("Masukan COM: ")
else:
    sp = "COM" + args.comport
    serPort = sp

if (args.baudrate == 0):
    baudRate = input("Masukan baudrate: ")
else:
    baudRate = args.baudrate

print(f"Program disetel untuk membuka koneksi dari {serPort} dengan baud rate {baudRate}.")

try:
    mavcom = mavutil.mavlink_connection(serPort, baudRate)
    print(f"\nMembuka port COM {serPort} dengan baud rate {baudRate}")
    mavudpout = mavutil.mavlink_connection("udpout:localhost:14550")
    print("Membuka port UDP pada 127.0.0.1:14550\n")
    # if(from_gcs):
    #     mavudpin = mavutil.mavlink_connection("udpin:localhost:14550")
    #     print("Membuka port UDP pada 127.0.0.1:14551\n")

except:
    print("Ada yang salah! Cek tulisan. Gunakan --help untuk membantu.")
    raise

'''
UNCOMMENT LISTING DI BAWAH JIKA INGIN MENGGUNAKAN
LIBRARY DARI PYTHON SECARA LANGSUNG

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.bind(('',socket.htons(14451)))

# master = mavutil.mavlink_connection()

# gc = sockaddr_in()
# gc.sin_family = socket.AF_INET
# gc.sin_addr = "127.0.0.1"
# gc.sin_port = socket.htons(14550)

# gcAddr = ("127.0.0.1", 14550)

# sock.connect(gcAddr)
'''

f = fifo()
mav = mavlink1.MAVLink(f)

print("Untuk menutup program, tekan CTRL+C pada keyboard.")
print()

while True:
    time_since_start += 100
    try:
        msg = mavcom.recv_msg()
        if(msg):
            print("Pesan diterima dari COM. ", end="")
            mavudpout.write(msg.get_msgbuf())
            print("| Pesan dikirim melalui UDP.")

        # if(from_gcs):
        #     msg_ = mavudpin.recv_msg()
        #     if (msg_):
        #         print(f"Received packet: SYS: {msg_.get_srcSystem()}, "
        #               f"COMP: {msg_.get_srcComponent()}, LEN: {len(msg_.get_msgbuf())}, "
        #               f"MSG ID: {msg_.get_msgId()}")
        '''
        BAGIAN INI ADALAH BAGIAN PENGIRIMAN PESAN 
        MAVLINK MENGGUNAKAN LIBRARY PYTHON
        
        # msg = mav.heartbeat_encode(mavlink1.MAV_TYPE_FIXED_WING, mavlink1.MAV_AUTOPILOT_GENERIC,
        #                            mavlink1.MAV_MODE_MANUAL_ARMED, 0, mavlink1.MAV_STATE_ACTIVE)
        # msg.pack(mav)
        # # sock.sendto(msg.get_msgbuf(), gcAddr)
        #
        # # msg = mav.attitude_encode(int(time_since_start), 1.12, 0.1, 2.71, 0., 0., 0.)
        # # msg.pack(mav)
        # # sock.sendto(msg.get_msgbuf(), gcAddr)
        #
        # msg = mav.param_value_encode(b'SYSID_THISMAV', 1., 0, 0, 0)
        # msg.pack(mav)
        # # sock.sendto(msg.get_msgbuf(), gcAddr)
        #
        # # data = sock.recvfrom(2048)
        # print("Bytes received: %d\nDatagaram: %a" %(len(data[0]), data[0].decode("ISO-8859-1")))
        # msg_ = mav.parse_char(data[0])
        # if(msg_):
        #     print(f"Received packet: SYS: {msg_.get_srcSystem()}, "
        #               f"COMP: {msg_.get_srcComponent()}, LEN: {len(msg_.get_msgbuf())}, "
        #               f"MSG ID: {msg_.get_msgId()}")
        # print()
        # # if(msg_.get_msgId() == 1):
        '''
        time.sleep(1)

    except KeyboardInterrupt:
        break

mavcom.close()
mavudpout.close()
print("Port serial ditutup.")