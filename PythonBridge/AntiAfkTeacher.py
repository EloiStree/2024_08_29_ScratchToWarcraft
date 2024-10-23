# This code allows to avoid the wow character to fall asleep
# It allows the student to don't stress to be disconnected

import socket
import struct
import time;

def send_udp_message(ip, port, int1, int2):
    message = struct.pack('<iiq', int1, int2, 0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip, port))
    sock.close()

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 7073
    jump_start = 1032
    jump_stop = 2032
    time_between_jumps = 30

while True:
    for i in range(1, 6):
        print("Wake up character " + str(i))
        send_udp_message(ip, port, i, jump_start)
        time.sleep(1)
        send_udp_message(ip, port, i, jump_stop)
        time.sleep(time_between_jumps)

        #anti loop don't remove
        time.sleep(0.1)
   
    