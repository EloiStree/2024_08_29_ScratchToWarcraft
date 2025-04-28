import asyncio
import websockets
import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#### RECEIVE
# What is the port number that the server will listen to?
server_websocket_port= 7072

#### SEND
# What is the port number that the server will send the data to?
#127.0.0.1 is your computer
#192.168.1.1 is your usualy a home device
#Make sure to be on the same LAN network.
targets_udp_ip =["127.0.0.1","192.168.1.111" ] 
# What is the port number that the server will send the data to?

server_websocket_port= 7072
target_udp_ip = "127.0.0.1"
target_udp_port = 7073


# Do you want some debug text ?
bool_display_received = True


print("Hello on the Websocke to UDP relay")
print(f"Port In: {server_websocket_port}")
print(f"Port Out: {target_udp_port}")


async def handler(websocket, path):
    byte_counter = 0
    print("Listening...")
    while True:
            global target_port
            data = await websocket.recv()
            try:
                # Relay received information to the UDP server
                for ip in targets_udp_ip:
                    udp_socket.sendto(data, (ip, target_udp_port))
                    # Count number of bytes sent to measure the traffic
                    byte_counter += 8 + len(data)
                
                if(bool_display_received):
                    print(f"Received {len(data)} | {data}")
                    print(f"Sent {byte_counter} bytes, {byte_counter/(1024)} KB, {byte_counter/(1024*1024)} MB")
                    print(f"Target: {targets_udp_ip}:{target_udp_port}")
            except ValueError:
                pass

# LOCALHOST: You only want to receive data from your own computer
lisentToAddressComingFrom="localhost"
# 0.0.0.0: You want to receive data from any computer
lisentToAddressComingFrom="0.0.0.0"

print(f"Start server... From {lisentToAddressComingFrom}:{server_websocket_port} to {targets_udp_ip}:{target_udp_port}")
while True:
    try:
        start_server = websockets.serve(handler, lisentToAddressComingFrom, server_websocket_port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except ValueError:
        print("Invalid input")            
