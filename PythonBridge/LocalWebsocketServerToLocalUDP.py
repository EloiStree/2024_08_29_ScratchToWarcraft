"""
pip install tornado
pip install websockets

"""

import tornado.ioloop
import tornado.web
import tornado.websocket
import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# WebSocket server port number
server_websocket_port = 7072

# Target IPs and target UDP port
targets_udp_ip = ["127.0.0.1", "192.168.1.111"]
target_udp_port = 7073

# Debug option
bool_display_received = True

print("Hello on the WebSocket to UDP relay")
print(f"WebSocket Listening Port: {server_websocket_port}")
print(f"UDP Target Port: {target_udp_port}")

# WebSocket handler to manage the WebSocket connections
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    byte_counter = 0  # Track the total number of bytes

    def open(self):
        print("WebSocket opened")
        self.write_message("Hello! WebSocket connected.")

    def on_message(self, message):
        # Relay received data to the UDP targets
        try:
            for ip in targets_udp_ip:
                udp_socket.sendto(message, (ip, target_udp_port))

            # Update the byte counter
            WebSocketHandler.byte_counter += len(message)

            if bool_display_received:
                print(f"Received {len(message)} bytes | {message}")
                print(f"Sent total {WebSocketHandler.byte_counter} bytes ({WebSocketHandler.byte_counter/1024:.2f} KB, {WebSocketHandler.byte_counter/(1024*1024):.2f} MB)")
                print(f"Targets: {targets_udp_ip} on port {target_udp_port}")
        except Exception as e:
            print(f"Error: {e}")

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        # Allow all origins
        return True

# Application setup
def make_app():
    return tornado.web.Application([
        (r"/", WebSocketHandler),
    ])

# Server setup
if __name__ == "__main__":
    print(f"Starting server... Listening on 0.0.0.0:{server_websocket_port}")
    app = make_app()
    app.listen(server_websocket_port)
    tornado.ioloop.IOLoop.current().start()

