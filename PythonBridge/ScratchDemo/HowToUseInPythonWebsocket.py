
import socket
import struct
import time

    
import asyncio
import websockets
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
ip_target_port = 7069

websocket_target = None

    
async def jump():
    await send_index_integer_command(int_character_index,int_jump_start)
    await asyncio.sleep(0.1)
    await send_index_integer_command(int_character_index,int_jump_stop)
    
async def forward(forward_running_time):
    await send_index_integer_command(int_character_index,int_forward_start)
    await asyncio.sleep(forward_running_time)
    await send_index_integer_command(int_character_index,int_forward_stop)

async def backward(forward_running_time):
    await send_index_integer_command(int_character_index,int_backward_start)
    await asyncio.sleep(forward_running_time)
    await send_index_integer_command(int_character_index,int_backward_stop)
    


async def send_index_integer_command( index:int, command:int):
    if websocket_target is None:
        return
    message = struct.pack('<ii', index, command)
    print(f"Sending {message}")
    print(f"Sending {index} {command}")
    await websocket_target.send(message)
    


async def running_loop_behaviour_with_websocket():
    global websocket_target
    global ip_target
    global ip_target_port
    uri= f"ws://{ip_target}:{ip_target_port}"
    async with websockets.connect(uri) as websocket:
        websocket_target = websocket
        while True:
    
            print("Jump")
            await jump()
            await asyncio.sleep(1)
            print("Forward")
            await forward(4)
            await asyncio.sleep(1)
            print("Backward")
            await backward(6)
            await asyncio.sleep(1)
    

if __name__ == "__main__":
    print("Starting...")
    asyncio.run(running_loop_behaviour_with_websocket())
    print("Done")


   
  
