import socket
import threading
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 3614
REDIRECT_IP = "127.0.0.1"
REDIRECT_PORT = 7073

additional_targets= {7072,7010}



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

redirect_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
redorect_sock_add = {}
for port in additional_targets:
    redorect_sock_add[port] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Listening on UDP port {UDP_PORT}")

total_bytes_received = 0
lock = threading.Lock()

kilo = 1024
mega = kilo * kilo
giga = kilo * mega
tera = kilo * giga

def display_bytes_count():
    global total_bytes_received
    while True:
        time.sleep(1)
        with lock:
            
            compress= total_bytes_received
            if compress < kilo:
                print(f"Total bytes received: {compress} B")
            elif compress < mega:
                print(f"Total bytes received: {compress / kilo} KB")
            elif compress < giga:
                print(f"Total bytes received: {compress / mega} MB")
            elif compress < tera:
                print(f"Total bytes received: {compress / giga} GB")
            else:
                print(f"Total bytes received: {compress / tera} TB")

            print(f"Total bytes received: {compress}")

# Start the thread
thread = threading.Thread(target=display_bytes_count)
thread.daemon = True
thread.start()

while True:
    data, addr = sock.recvfrom(8096)  # buffer size is 8096 bytes
    with lock:
        total_bytes_received += len(data)
    redirect_sock.sendto(data, (REDIRECT_IP, REDIRECT_PORT))
    for port in additional_targets:
        redorect_sock_add[port].sendto(data, (REDIRECT_IP, port))
