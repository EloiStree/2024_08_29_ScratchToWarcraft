import asyncio
import websockets
import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_websocket_port= 7072
target_udp_ip = "127.0.0.1"
target_udp_port = 7073
bool_display_received = True



async def handler(websocket, path):
    byte_counter = 0
    while True:
            global target_port
            data = await websocket.recv()
            try:
                udp_socket.sendto(data, (target_udp_ip, target_udp_port))
                byte_counter += 8 + len(data)
                if(bool_display_received):
                    print(f"Received {len(data)} | {data}")
                    print(f"Sent {byte_counter} bytes, {byte_counter/(1024)} KB, {byte_counter/(1024*1024)} MB")
                    print(f"Target: {target_udp_ip}:{target_udp_port}")
            except ValueError:
                pass
            
start_server = websockets.serve(handler, "localhost", server_websocket_port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()