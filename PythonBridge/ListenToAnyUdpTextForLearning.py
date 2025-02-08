import socket

# Define the IP address and port number
UDP_IP = "0.0.0.0"
UDP_PORT = 7072

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Get the current IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Current IP Address: {local_ip}")


print(f"Listening on {UDP_IP}:{UDP_PORT}")

while True:
    # Receive data from the socket
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print(f"Received message: {data} from {addr}")