
import socket
import struct
import time


int_character_index =1
int_jump_start= 1032
int_jump_stop =2032
int_forward_start = 1038
int_forward_stop = 2038
int_backward_start = 1040
int_backward_stop = 2040


ip_target ="127.0.0.1"
ip_target_port = 7073


def send_index_integer_command( int1, int2):
    message = struct.pack('<iiq', int1, int2, 0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip_target, ip_target_port))
    sock.close()

# Sent Little Endian Integer to target
def send_index_integer_command_with_ip(ip, port, int1, int2):
    message = struct.pack('<iiq', int1, int2, 0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip, port))
    sock.close()
    
def jump():
    send_index_integer_command(int_character_index,int_jump_start)
    time.sleep(0.1)
    send_index_integer_command(int_character_index,int_jump_stop)
    
def forward(forward_running_time):
    send_index_integer_command(int_character_index,int_forward_start)
    time.sleep(forward_running_time)
    send_index_integer_command(int_character_index,int_forward_stop)
def backward(forward_running_time):
    send_index_integer_command(int_character_index,int_backward_start)
    time.sleep(forward_running_time)
    send_index_integer_command(int_character_index,int_backward_stop)
    

while True:
    print("Jump")
    jump()
    time.sleep(1)
    print("Forward")
    forward(4)
    time.sleep(1)
    print("Backward")
    backward(6)
    time.sleep(1)