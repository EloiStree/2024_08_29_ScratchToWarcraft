import socket
import time

def send_udp_message():
    # Define the server address and port
    server_address = ('127.0.0.1', 7031)
    message = "Hello, World!"

    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        try:
            # Add a delay of 1 second before sending the message
            print("Waiting for 1 second...")
            time.sleep(1)

            # Send the message
            print(f"Sending message to {server_address}: {message}")
            udp_socket.sendto(message.encode('utf-8'), server_address)
            print("Message sent successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_udp_message()
