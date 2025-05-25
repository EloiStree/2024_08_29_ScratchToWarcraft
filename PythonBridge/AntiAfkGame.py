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

int_space_key = 1088
int_x_key = 1088

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 7073
    action_cancel_afk = int_x_key
    time_between_jumps = 30

    while True:
        for i in range(1,9):
            print("Wake up character " + str(i))
            send_udp_message(ip, port, i, action_cancel_afk)
            time.sleep(1)
            send_udp_message(ip, port, i, action_cancel_afk+1000)
            time.sleep(time_between_jumps)

            #anti loop don't remove
            time.sleep(0.1)
    
    
