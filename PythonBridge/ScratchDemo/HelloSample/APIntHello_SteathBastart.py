# Game: https://store.steampowered.com/app/209190/Stealth_Bastard_Deluxe/

# https://pypi.org/project/iid42/
from iid42 import *
# https://pypi.org/project/wowint/
from wowint import WowIntegerTarget, WowIntegerKeyboard

import socket
import struct
import time

target_udp = "127.0.0.1"
target_port = 7073
player_index =0

key_left = WowIntegerKeyboard.arrow_left
key_right = WowIntegerKeyboard.arrow_right
key_up = WowIntegerKeyboard.arrow_up
key_down = WowIntegerKeyboard.arrow_down
key_jump = WowIntegerKeyboard.key_a
key_carry = WowIntegerKeyboard.key_z
key_gadget = WowIntegerKeyboard.key_e
key_restart = WowIntegerKeyboard.key_r
key_enter = WowIntegerKeyboard.enter
key_escape = WowIntegerKeyboard.escape
sender = SendUdpIID(target_udp, target_port,True)

## When you leave the game it trigger main menu, so you need to press enter to go back to the game.

bool_use_start_escape = False
if bool_use_start_escape:
    time.sleep(1)
    sender.push_index_integer( player_index,key_escape)
    sender.push_index_integer( player_index,key_enter)
    time.sleep(1)
    sender.push_index_integer(player_index,key_escape+1000)
    sender.push_index_integer(player_index,key_enter+1000)

# Let's restart the level.
time.sleep(1)

while True:

    bool_full_level = True
    if bool_full_level:
        time.sleep(1)
        sender.push_index_integer( player_index,key_restart)
        time.sleep(1)
        sender.push_index_integer(player_index,key_restart+1000)

        time.sleep(18)
        sender.push_index_integer( player_index,key_right)
        time.sleep(4)
        sender.push_index_integer(player_index,key_right+1000)

        time.sleep(6)
        sender.push_index_integer( player_index,key_left)
        time.sleep(1)
        sender.push_index_integer(player_index,key_left+1000)

        sender.push_index_integer( player_index,key_jump)
        time.sleep(1)
        sender.push_index_integer(player_index,key_jump+1000)
        time.sleep(2)
        
        sender.push_index_integer( player_index,key_right)
        time.sleep(4)
        sender.push_index_integer(player_index,key_right+1000)
        time.sleep(1)
        sender.push_index_integer( player_index,key_left)
        time.sleep(5)
        sender.push_index_integer(player_index,key_left+1000)
        
        time.sleep(5)
        sender.push_index_integer( player_index,key_right)
        time.sleep(0.65)
        sender.push_index_integer( player_index,key_jump)
        time.sleep(2)
        sender.push_index_integer( player_index,key_jump+1000)
        time.sleep(1)
        sender.push_index_integer( player_index,key_right+1000)
        
        sender.push_index_integer( player_index,key_right)
        time.sleep(0.7)
        sender.push_index_integer( player_index,key_jump)
        time.sleep(2)
        sender.push_index_integer( player_index,key_jump+1000)
        sender.push_index_integer( player_index,key_right+1000)
            

        sender.push_index_integer( player_index,key_right+1000)
        sender.push_index_integer( player_index,key_left)
        time.sleep(0.3)
        sender.push_index_integer(player_index,key_left+1000)
        sender.push_index_integer( player_index,key_up)
        time.sleep(3)
        sender.push_index_integer(player_index,key_up+1000)
        
        sender.push_index_integer( player_index,key_left)
        time.sleep(3)
        sender.push_index_integer(player_index,key_left+1000)

    time.sleep(8)
        





