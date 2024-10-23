import ctypes
import time
import socket
import pyperclip
import psutil
import pygetwindow as gw
import asyncio
import threading



## Port that app is listening to be used
lisent_udp_port_to_interact = 7073
## What is the exact name to find in of the window we need to find.
window_title = "World of Warcraft"

debug_at_pression_send=True


use_print_log=True


player_index_to_window_index ={}

## use to broadcast on target window from source index id
player_index_to_window_index [0]= [0,1,2,3]
player_index_to_window_index [1]= [0]
player_index_to_window_index [2]= [1]
player_index_to_window_index [3]= [2]
player_index_to_window_index [4]= [3]
player_index_to_window_index [10]= [0,1,2,3,4,5,6,7,8,9,10,11]






























user32 = ctypes.windll.user32

## ## ## ## ## ## ## ## 
##  PUBLIC
## ## ## ## ## ## ## ## 

## What window index should we use ?
target_window_index = 0


#window_title = "10 Second Ninja"
## window_title = "MORDHAU  "
## window_title = "Hollow Knight"
## window_title = "Chrome"







######################### NE PAS TOUCHER ############################
######################### DONT TOUCH ############################


# Use real will simulate key, use false will send fake key

# Constants for SendMessage
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101



# Find the window by its title
def find_window(title):
    return ctypes.windll.user32.FindWindowW(None, title)


def get_all_windows(title):
    list_window_found = [window for window in gw.getAllWindows() if title in window.title]
    return list_window_found



def find_in_all(title):
    global target_window_index
    list_window_found = [window for window in gw.getAllWindows() if title in window.title]
    if list_window_found:
        return list_window_found[0]
    else:
        return None
    
    
def find_in_all(title, index):
    global target_window_index
    list_window_found = [window for window in gw.getAllWindows() if title in window.title]
    if list_window_found and len(list_window_found) > index:
        return list_window_found[index]
    else:
        return None
def find_in_all_count(title):
    global target_window_index
    list_window_found = [window for window in gw.getAllWindows() if title in window.title]
    if list_window_found :
        return len(list_window_found)
    else:
        return 0





all_found_windows_at_start = get_all_windows(window_title)



first_window_foundhwnd = find_window(window_title)
found_window_count= find_in_all_count(window_title)


print (f"Window found:{first_window_foundhwnd} Count:{found_window_count}")

for windowt in all_found_windows_at_start:
    print("Window Title:", windowt.title)
    print("Window ID:", windowt._hWnd)


# Define the necessary structures
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Define the necessary functions
def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


























timebetweenaction=0.1
timepress=0.1




def enum_child_windows(parent_hwnd):
    child_windows = []

    def enum_child_proc(hwnd, lParam):
        nonlocal child_windows
        child_windows.append(hwnd)
        return True  # Continue enumeration

    # Convert the callback function to a C function pointer
    EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    # Call EnumChildWindows with the parent window handle and the callback function
    ctypes.windll.user32.EnumChildWindows(parent_hwnd, EnumChildProc(enum_child_proc), 0)

    return child_windows

def is_window_focused(hwnd):
    return user32.GetForegroundWindow() == hwnd

# def send_key(hwnd, key_code):
    
#         child_windows = enum_child_windows(hwnd)
#         # for child_hwnd in child_windows:
#         #     send_key_press(child_hwnd, key_code)
#         #     time.sleep(0.1)  # Optional delay between keydown and keyup
#         #     send_key_release(child_hwnd, key_code)

def send_key_press(hwnd, key_code):
   
        
        
        ctypes.windll.user32.PostMessageW(int(hwnd), WM_KEYDOWN, int(key_code), 0)
        # child_windows = enum_child_windows(hwnd)
        # for child_hwnd in child_windows:
        #     print(f"       Press child {str(hex_value)} to {child_hwnd }")  
        #     ctypes.windll.user32.PostMessageW(child_hwnd, WM_KEYDOWN, char_value, 0)

def send_key_release(hwnd, key_code):
   
        ctypes.windll.user32.PostMessageW(int(hwnd), WM_KEYUP, int(key_code), 0)
        # child_windows = enum_child_windows(hwnd)
        # for child_hwnd in child_windows:
        #     print(f"       Release child {str(hex_value)} to {child_hwnd }")  
        #     ctypes.windll.user32.PostMessageW(child_hwnd, WM_KEYUP, char_value, 0)



def check_and_copy(message):
    if message.startswith("c "):
        content = message[2:]  # Extract the content after "c "
        pyperclip.copy(content)
        if use_print_log:
            print("Content copied to clipboard:", content)
        return True
    else:
        return False


    

def push_to_all_integer(int_value):
    for key in player_index_to_window_index:
        push_to_index_integer(key,int_value )

def push_test(window, press, key_id):
    global debug_at_pression_send
    

    
    print(f"Test {press} {key_id} to {window.title} / {window._hWnd}")
    if window:
        if press==True:
            if debug_at_pression_send:
                print(f"Press {key_id} to {window.title}")
            send_key_press(window._hWnd, key_id)
        else:
            if debug_at_pression_send:
                print(f"Release {key_id} to {window.title}")
            send_key_release(window._hWnd, key_id)
            


def push_to_index_integer(int_index, int_value):
    global keyboard_mappings
    #print("start")
    #print(f"R | Index {int_index}| Value {int_value}")
    key_name_last_found=""
    press_last_found=False
    one_found=False
    
    key_info = key_map.try_to_guess_key(str(int_value))
    if key_info is None or key_info[0] is None:
        return
        
    
    print(f"Push {int_value} to Window {int_index} ({key_info[0].name} / {key_info[0].hexadecimal})")
    print(f"Push {key_info[0]}")

    ## Is player index existing in register
    if( int_index in player_index_to_window_index):
        ## Get the list of window index for this player to broadcast
        window_index_list = player_index_to_window_index[int_index]
        ## For each window index to broadcast
        for window_index in window_index_list:
            ## If the window index in range of existing one at start
            if window_index < len(all_found_windows_at_start):
                    ## If the value is existing in the mapping allows to player
                    int_value_as_string = str(int_value)
                    
                    print (f"{int_value}  {key_info[1]}   {key_info[2]}")
                    
                    if key_info[1]:
                        push_test(all_found_windows_at_start[window_index], True, key_info[0].decimal)
                        
                    if key_info[2]:
                        push_test(all_found_windows_at_start[window_index], False, key_info[0].decimal)
                        
        #if(one_found):
        #    print(f"Index {int_index} | Value {int_value} | Key {key_name_last_found} | Press {press_last_found}")
  
   # print("Stop")






async def async_task():
        
        print("Async task started")
        await asyncio.sleep(2)
        print("Async task ready")
        
        # Launch the async task

        for key in list(keyboard_mappings.keys()):
            keyboard_mappings[key.lower().replace(" ", "")] = keyboard_mappings.pop(key)

        # Define the UDP IP address and port to listen on
        UDP_IP = "127.0.0.1" 
        

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        sock.bind((UDP_IP, lisent_udp_port_to_interact))


        print("UDP server listening on port", lisent_udp_port_to_interact)

        try:
            while True:
                data, addr = sock.recvfrom(1024)  
                
                byte_counter = len(data)
                #print("received message:", data)  
                print(f"R| {len(data)} | {data}")
                if byte_counter == 4:
                    int_value = int.from_bytes(data, byteorder='little')
                    if use_print_log:
                        print(f"Value {int_value} ")
                    push_to_all_integer(int_value)
                    
                elif  byte_counter==12:

                    int_value= int.from_bytes(data[0:4], byteorder='little')
                    long_data_2= int.from_bytes(data[4:12], byteorder='little')
                    push_to_all_integer(int_value)
                    if use_print_log:
                        print("Value ",int_value)
                        
                elif  byte_counter==16:

                    int_index= int.from_bytes(data[0:4], byteorder='little')
                    int_value= int.from_bytes(data[4:8], byteorder='little')
                    long_data_2= int.from_bytes(data[8:16], byteorder='little')
                    if use_print_log :
                        print("Index ",int_index,"Value",int_value)
                    push_to_index_integer(int_index, int_value)
                    # thread = threading.Thread(target=push_to_index_integer, args=(int_index, int_value))
                    # thread.start()



           
                
                    
        except KeyboardInterrupt:
            print("Server stopped.")
        

class KeyInfo:
    def __init__(self, name, decimal, hexadecimal, press, release):
        self.name = name
        self.decimal = decimal
        self.hexadecimal = hexadecimal
        self.press = press
        self.release = release
        
      
            

    def __repr__(self):
        return f"KeyInfo(name='{self.name}', decimal={self.decimal}, hexadecimal='{self.hexadecimal}', press={self.press}, release={self.release})"


class KeyMap:
    def __init__(self):
        self.keys = {
            "Backspace": KeyInfo("Backspace", 8, 0x08, 1008, 2008),
            "Tab": KeyInfo("Tab", 9, 0x09, 1009, 2009),
            "Clear": KeyInfo("Clear", 12, 0x0C, 1012, 2012),
            "Enter": KeyInfo("Enter", 13, 0x0D, 1013, 2013),
            "Shift": KeyInfo("Shift", 16, 0x10, 1016, 2016),
            "Ctrl": KeyInfo("Ctrl", 17, 0x11, 1017, 2017),
            "Alt": KeyInfo("Alt", 18, 0x12, 1018, 2018),
            "Pause": KeyInfo("Pause", 19, 0x13, 1019, 2019),
            "CapsLock": KeyInfo("CapsLock", 20, 0x14, 1020, 2020),
            "Esc": KeyInfo("Esc", 27, 0x1B, 1027, 2027),
            "Escape": KeyInfo("Escape", 27, 0x1B, 1027, 2027),
            "Space": KeyInfo("Space", 32, 0x20, 1032, 2032),
            "PageUp": KeyInfo("PageUp", 33, 0x21, 1033, 2033),
            "PageDown": KeyInfo("PageDown", 34, 0x22, 1034, 2034),
            "End": KeyInfo("End", 35, 0x23, 1035, 2035),
            "Home": KeyInfo("Home", 36, 0x24, 1036, 2036),
            "LeftArrow": KeyInfo("LeftArrow", 37, 0x25, 1037, 2037),
            "Left": KeyInfo("Left", 37, 0x25, 1037, 2037),
            "UpArrow": KeyInfo("UpArrow", 38, 0x26, 1038, 2038),
            "Up": KeyInfo("Up", 38, 0x26, 1038, 2038),
            "RightArrow": KeyInfo("RightArrow", 39, 0x27, 1039, 2039),
            "Right": KeyInfo("Right", 39, 0x27, 1039, 2039),
            "DownArrow": KeyInfo("DownArrow", 40, 0x28, 1040, 2040),
            "Down": KeyInfo("Down", 40, 0x28, 1040, 2040),
            "Select": KeyInfo("Select", 41, 0x29, 1041, 2041),
            "Print": KeyInfo("Print", 42, 0x2A, 1042, 2042),
            "Execute": KeyInfo("Execute", 43, 0x2B, 1043, 2043),
            "PrintScreen": KeyInfo("PrintScreen", 44, 0x2C, 1044, 2044),
            "Insert": KeyInfo("Insert", 45, 0x2D, 1045, 2045),
            "Delete": KeyInfo("Delete", 46, 0x2E, 1046, 2046),
            "0": KeyInfo("0", 48, 0x30, 1048, 2048),
            "1": KeyInfo("1", 49, 0x31, 1049, 2049),
            "2": KeyInfo("2", 50, 0x32, 1050, 2050),
            "3": KeyInfo("3", 51, 0x33, 1051, 2051),
            "4": KeyInfo("4", 52, 0x34, 1052, 2052),
            "5": KeyInfo("5", 53, 0x35, 1053, 2053),
            "6": KeyInfo("6", 54, 0x36, 1054, 2054),
            "7": KeyInfo("7", 55, 0x37, 1055, 2055),
            "8": KeyInfo("8", 56, 0x38, 1056, 2056),
            "9": KeyInfo("9", 57, 0x39, 1057, 2057),
            "A": KeyInfo("A", 65, 0x41, 1065, 2065),
            "B": KeyInfo("B", 66, 0x42, 1066, 2066),
            "C": KeyInfo("C", 67, 0x43, 1067, 2067),
            "D": KeyInfo("D", 68, 0x44, 1068, 2068),
            "E": KeyInfo("E", 69, 0x45, 1069, 2069),
            "F": KeyInfo("F", 70, 0x46, 1070, 2070),
            "G": KeyInfo("G", 71, 0x47, 1071, 2071),
            "H": KeyInfo("H", 72, 0x48, 1072, 2072),
            "I": KeyInfo("I", 73, 0x49, 1073, 2073),
            "J": KeyInfo("J", 74, 0x4A, 1074, 2074),
            "K": KeyInfo("K", 75, 0x4B, 1075, 2075),
            "L": KeyInfo("L", 76, 0x4C, 1076, 2076),
            "M": KeyInfo("M", 77, 0x4D, 1077, 2077),
            "N": KeyInfo("N", 78, 0x4E, 1078, 2078),
            "O": KeyInfo("O", 79, 0x4F, 1079, 2079),
            "P": KeyInfo("P", 80, 0x50, 1080, 2080),
            "Q": KeyInfo("Q", 81, 0x51, 1081, 2081),
            "R": KeyInfo("R", 82, 0x52, 1082, 2082),
            "S": KeyInfo("S", 83, 0x53, 1083, 2083),
            "T": KeyInfo("T", 84, 0x54, 1084, 2084),
            "U": KeyInfo("U", 85, 0x55, 1085, 2085),
            "V": KeyInfo("V", 86, 0x56, 1086, 2086),
            "W": KeyInfo("W", 87, 0x57, 1087, 2087),
            "X": KeyInfo("X", 88, 0x58, 1088, 2088),
            "Y": KeyInfo("Y", 89, 0x59, 1089, 2089),
            "Z": KeyInfo("Z", 90, 0x5A, 1090, 2090),
            "LeftWindows": KeyInfo("LeftWindows", 91, 0x5B, 1091, 2091),
            "RightWindows": KeyInfo("RightWindows", 92, 0x5C, 1092, 2092),
            "Applications": KeyInfo("Applications", 93, 0x5D, 1093, 2093),
            "Sleep": KeyInfo("Sleep", 95, 0x5F, 1095, 2095),
            "Numpad0": KeyInfo("Numpad0", 96, 0x60, 1096, 2096),
            "Numpad1": KeyInfo("Numpad1", 97, 0x61, 1097, 2097),
            "Numpad2": KeyInfo("Numpad2", 98, 0x62, 1098, 2098),
            "Numpad3": KeyInfo("Numpad3", 99, 0x63, 1099, 2099),
            "Numpad4": KeyInfo("Numpad4", 100, 0x64, 1100, 2100),
            "Numpad5": KeyInfo("Numpad5", 101, 0x65, 1101, 2101),
            "Numpad6": KeyInfo("Numpad6", 102, 0x66, 1102, 2102),
            "Numpad7": KeyInfo("Numpad7", 103, 0x67, 1103, 2103),
            "Numpad8": KeyInfo("Numpad8", 104, 0x68, 1104, 2104),
            "Numpad9": KeyInfo("Numpad9", 105, 0x69, 1105, 2105),
            "Multiply": KeyInfo("Multiply", 106, 0x6A, 1106, 2106),
            "Add": KeyInfo("Add", 107, 0x6B, 1107, 2107),
            "Separator": KeyInfo("Separator", 108, 0x6C, 1108, 2108),
            "Subtract": KeyInfo("Subtract", 109, 0x6D, 1109, 2109),
            "Decimal": KeyInfo("Decimal", 110, 0x6E, 1110, 2110),
            "Divide": KeyInfo("Divide", 111, 0x6F, 1111, 2111),
            "F1": KeyInfo("F1", 112, 0x70, 1112, 2112),
            "F2": KeyInfo("F2", 113, 0x71, 1113, 2113),
            "F3": KeyInfo("F3", 114, 0x72, 1114, 2114),
            "F4": KeyInfo("F4", 115, 0x73, 1115, 2115),
            "F5": KeyInfo("F5", 116, 0x74, 1116, 2116),
            "F6": KeyInfo("F6", 117, 0x75, 1117, 2117),
            "F7": KeyInfo("F7", 118, 0x76, 1118, 2118),
            "F8": KeyInfo("F8", 119, 0x77, 1119, 2119),
            "F9": KeyInfo("F9", 120, 0x78, 1120, 2120),
            "F10": KeyInfo("F10", 121, 0x79, 1121, 2121),
            "F11": KeyInfo("F11", 122, 0x7A, 1122, 2122),
            "F12": KeyInfo("F12", 123, 0x7B, 1123, 2123),
            "F13": KeyInfo("F13", 124, 0x7C, 1124, 2124),
            "F14": KeyInfo("F14", 125, 0x7D, 1125, 2125),
            "F15": KeyInfo("F15", 126, 0x7E, 1126, 2126),
            "F16": KeyInfo("F16", 127, 0x7F, 1127, 2127),
            "F17": KeyInfo("F17", 128, 0x80, 1128, 2128),
            "F18": KeyInfo("F18", 129, 0x81, 1129, 2129),
            "F19": KeyInfo("F19", 130, 0x82, 1130, 2130),
            "F20": KeyInfo("F20", 131, 0x83, 1131, 2131),
            "F21": KeyInfo("F21", 132, 0x84, 1132, 2132),
            "F22": KeyInfo("F22", 133, 0x85, 1133, 2133),
            "F23": KeyInfo("F23", 134, 0x86, 1134, 2134),
            "F24": KeyInfo("F24", 135, 0x87, 1135, 2135),
            "NumLock": KeyInfo("NumLock", 144, 0x90, 1144, 2144),
            "ScrollLock": KeyInfo("ScrollLock", 145, 0x91, 1145, 2145),
            "LeftShift": KeyInfo("LeftShift", 160, 0xA0, 1160, 2160),
            "RightShift": KeyInfo("RightShift", 161, 0xA1, 1161, 2161),
            "LeftCtrl": KeyInfo("LeftCtrl", 162, 0xA2, 1162, 2162),
            "RightCtrl": KeyInfo("RightCtrl", 163, 0xA3, 1163, 2163),
            "LeftMenu": KeyInfo("LeftMenu", 164, 0xA4, 1164, 2164),
            "RightMenu": KeyInfo("RightMenu", 165, 0xA5, 1165, 2165),
            "BrowserBack": KeyInfo("BrowserBack", 166, 0xA6, 1166, 2166),
            "BrowserForward": KeyInfo("BrowserForward", 167, 0xA7, 1167, 2167),
            "BrowserRefresh": KeyInfo("BrowserRefresh", 168, 0xA8, 1168, 2168),
            "BrowserStop": KeyInfo("BrowserStop", 169, 0xA9, 1169, 2169),
            "BrowserSearch": KeyInfo("BrowserSearch", 170, 0xAA, 1170, 2170),
            "BrowserFavorites": KeyInfo("BrowserFavorites", 171, 0xAB, 1171, 2171),
            "BrowserHome": KeyInfo("BrowserHome", 172, 0xAC, 1172, 2172),
            "VolumeMute": KeyInfo("VolumeMute", 173, 0xAD, 1173, 2173),
            "VolumeDown": KeyInfo("VolumeDown", 174, 0xAE, 1174, 2174),
            "VolumeUp": KeyInfo("VolumeUp", 175, 0xAF, 1175, 2175),
            "MediaNextTrack": KeyInfo("MediaNextTrack", 176, 0xB0, 1176, 2176),
            "MediaPrevTrack": KeyInfo("MediaPrevTrack", 177, 0xB1, 1177, 2177),
            "MediaStop": KeyInfo("MediaStop", 178, 0xB2, 1178, 2178),
            "MediaPlayPause": KeyInfo("MediaPlayPause", 179, 0xB3, 1179, 2179),
            "LaunchMail": KeyInfo("LaunchMail", 180, 0xB4, 1180, 2180),
            "LaunchMediaSelect": KeyInfo("LaunchMediaSelect", 181, 0xB5, 1181, 2181),
            "LaunchApp1": KeyInfo("LaunchApp1", 182, 0xB6, 1182, 2182),
            "LaunchApp2": KeyInfo("LaunchApp2", 183, 0xB7, 1183, 2183),
        }

    def get_key_info(self, key_name):
        return self.keys.get(key_name, None)
    
    def find_key_in_press(self, press):
        for key_info in self.keys.values():
            if key_info.press == press:
                return key_info
        return None
    
    def find_key_in_release(self, release):
        for key_info in self.keys.values():
            if key_info.release == release:
                return key_info
        return None
    
    def find_key_in_decimal(self, decimal):
        for key_info in self.keys.values():
            if key_info.decimal == decimal:
                return key_info
        return None
    
    def find_key_in_hexadecimal(self, hexadecimal):
        for key_info in self.keys.values():
            if key_info.hexadecimal == hexadecimal:
                return key_info
        return None
    
    def find_key_in_name(self, name):
        for key_info in self.keys.values():
            if key_info.name == name:
                return key_info
        return None
    
    def find_key_in_name_lower(self, name):
        name = name.lower()
        for key_info in self.keys.values():
            if key_info.name.lower() == name:
                return key_info
        return None
    
    def try_to_guess_key(self, key):
       
        key= key.lower().replace(" ", "")
        key_info = self.find_key_in_press(key)
        if(key_info is not None):
            return key_info, True, False
        
        key_info = self.find_key_in_release(key)
        if(key_info is not None):
            return key_info, False , True
        
        
        key_info = self.find_key_in_hexadecimal(key)
        if(key_info is not None):
            return key_info,True, True
        
        
        key_info = self.find_key_in_decimal(key)
        if(key_info is not None):
            return key_info,True, True
        
        key_info = self.find_key_in_name(key)
        if(key_info is not None):
            return key_info,True, True
        
        key_info = self.find_key_in_name_lower(key)
        if(key_info is not None):
            return key_info,True, True

key_map = KeyMap()


def remove_spaces(text: str) -> str:
    return str(text.replace(" ", "").lower())

for key_info in key_map.keys:
    key_map.keys[key_info].name = remove_spaces(str(key_map.keys[key_info].name))
    key_map.keys[key_info].press = remove_spaces(str(key_map.keys[key_info].press))
    key_map.keys[key_info].release = remove_spaces(str(key_map.keys[key_info].release))
    key_map.keys[key_info].hexadecimal = remove_spaces(str(key_map.keys[key_info].hexadecimal))
    key_map.keys[key_info].decimal = remove_spaces(str(key_map.keys[key_info].decimal))
    
key_info= key_map.get_key_info("Enter")
print("ID",key_info)

key_info = key_map.try_to_guess_key("1013")
print("Press",key_info)

key_info = key_map.try_to_guess_key("2013")
print("Release",key_info)

key_info = key_map.try_to_guess_key("0x0D")
print("Decimal",key_info)

key_info = key_map.try_to_guess_key("13")
print("Integer",key_info)

key_info = key_map.try_to_guess_key("Enter")
print("Name case",key_info)

key_info = key_map.try_to_guess_key("enter")
print("Name no case",key_info)


    

if __name__ == "__main__":
   
    keyboard_mappings = {
    "Backspace": 0x08,
    "Tab": 0x09,
    "Clear": 0x0C,
    "Enter": 0x0D,
    "Shift": 0x10,
    "Ctrl": 0x11,
    "Alt": 0x12,
    "Pause": 0x13,
    "CapsLock": 0x14,
    "Esc": 0x1B,
    "Escape": 0x1B,
    "Space": 0x20,
    "PageUp": 0x21,
    "PageDown": 0x22,
    "End": 0x23,
    "Home": 0x24,
    "LeftArrow": 0x25,
    "Left": 0x25,
    "UpArrow": 0x26,
    "Up": 0x26,
    "RightArrow": 0x27,
    "Right": 0x27,
    "DownArrow": 0x28,
    "Down": 0x28,
    "Select": 0x29,
    "Print": 0x2A,
    "Execute": 0x2B,
    "PrintScreen": 0x2C,
    "Insert": 0x2D,
    "Delete": 0x2E,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'A': 0x41,
    'B': 0x42,
    'C': 0x43,
    'D': 0x44,
    'E': 0x45,
    'F': 0x46,
    'G': 0x47,
    'H': 0x48,
    'I': 0x49,
    'J': 0x4A,
    'K': 0x4B,
    'L': 0x4C,
    'M': 0x4D,
    'N': 0x4E,
    'O': 0x4F,
    'P': 0x50,
    'Q': 0x51,
    'R': 0x52,
    'S': 0x53,
    'T': 0x54,
    'U': 0x55,
    'V': 0x56,
    'W': 0x57,
    'X': 0x58,
    'Y': 0x59,
    'Z': 0x5A,
    "LeftWindows": 0x5B,
    "RightWindows": 0x5C,
    "Applications": 0x5D,
    "Sleep": 0x5F,
    "Numpad0": 0x60,
    "Numpad1": 0x61,
    "Numpad2": 0x62,
    "Numpad3": 0x63,
    "Numpad4": 0x64,
    "Numpad5": 0x65,
    "Numpad6": 0x66,
    "Numpad7": 0x67,
    "Numpad8": 0x68,
    "Numpad9": 0x69,
    "Multiply": 0x6A,
    "NP0": 0x60,
    "NP1": 0x61,
    "NP2": 0x62,
    "NP3": 0x63,
    "NP4": 0x64,
    "NP5": 0x65,
    "NP6": 0x66,
    "NP7": 0x67,
    "NP8": 0x68,
    "NP9": 0x69,
    "Multiply": 0x6A,
    "Add": 0x6B,
    "Separator": 0x6C,
    "Subtract": 0x6D,
    "Decimal": 0x6E,
    "Divide": 0x6F,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
    "F13": 0x7C,
    "F14": 0x7D,
    "F15": 0x7E,
    "F16": 0x7F,
    "F17": 0x80,
    "F18": 0x81,
    "F19": 0x82,
    "F20": 0x83,
    "F21": 0x84,
    "F22": 0x85,
    "F23": 0x86,
    "F24": 0x87,
    "NumLock": 0x90,
    "ScrollLock": 0x91,
    "LeftShift": 0xA0,
    "RightShift": 0xA1,
    "LeftControl": 0xA2,
    "RightControl": 0xA3,
    "LeftAlt": 0xA4,
    "RightAlt": 0xA5,
    "LeftMenu": 0xA4,
    "RightMenu": 0xA5,
    "BrowserBack": 0xA6,
    "BrowserForward": 0xA7,
    "BrowserRefresh": 0xA8,
    "BrowserStop": 0xA9,
    "BrowserSearch": 0xAA,
    "BrowserFavorites": 0xAB,
    "BrowserHome": 0xAC,
    "VolumeMute": 0xAD,
    "VolumeDown": 0xAE,
    "VolumeUp": 0xAF,
    "MediaNext Track": 0xB0,
    "MediaPrevious Track": 0xB1,
    "MediaStop": 0xB2,
    "MediaPlay": 0xB3,
    "LaunchMail": 0xB4,
    "LaunchMedia Select": 0xB5,
    "LaunchApp1": 0xB6,
    "LaunchApp2": 0xB7,
    "OEM1": 0xBA,
    "OEMPlus": 0xBB,
    "OEMComma": 0xBC,
    "OEMMinus": 0xBD,
    "OEMPeriod": 0xBE,
    "OEM2": 0xBF,
    "OEM3": 0xC0,
    "OEM4": 0xDB,
    "OEM5": 0xDC,
    "OEM6": 0xDD,
    "OEM7": 0xDE,
    "OEM8": 0xDF,
    "OEM102": 0xE2,
    "ProcessKey": 0xE5,
    "Packet": 0xE7,
    "Attn": 0xF6,
    "CrSel": 0xF7,
    "ExSel": 0xF8,
    "EraseEOF": 0xF9,
    "Play": 0xFA,
    "Zoom": 0xFB,
    "PA1": 0xFD,
    "0x08":"0x08",
    "0x09":"0x09",
    "0x0C":"0x0C",
    "0x0D":"0x0D",
    "0x10":"0x10",
    "0x11":"0x11",
    "0x12":"0x12",
    "0x13":"0x13",
    "0x14":"0x14",
    "0x1B":"0x1B",
    "0x20":"0x20",
    "0x21":"0x21",
    "0x22":"0x22",
    "0x23":"0x23",
    "0x24":"0x24",
    "0x25":"0x25",
    "0x26":"0x26",
    "0x27":"0x27",
    "0x28":"0x28",
    "0x29":"0x29",
    "0x2A":"0x2A",
    "0x2B":"0x2B",
    "0x2C":"0x2C",
    "0x2D":"0x2D",
    "0x2E":"0x2E",
    "0x30":"0x30",
    "0x31":"0x31",
    "0x32":"0x32",
    "0x33":"0x33",
    "0x34":"0x34",
    "0x35":"0x35",
    "0x36":"0x36",
    "0x37":"0x37",
    "0x38":"0x38",
    "0x39":"0x39",
    "0x41":"0x41",
    "0x42":"0x42",
    "0x43":"0x43",
    "0x44":"0x44",
    "0x45":"0x45",
    "0x46":"0x46",
    "0x47":"0x47",
    "0x48":"0x48",
    "0x49":"0x49",
    "0x4A":"0x4A",
    "0x4B":"0x4B",
    "0x4C":"0x4C",
    "0x4D":"0x4D",
    "0x4E":"0x4E",
    "0x4F":"0x4F",
    "0x50":"0x50",
    "0x51":"0x51",
    "0x52":"0x52",
    "0x53":"0x53",
    "0x54":"0x54",
    "0x55":"0x55",
    "0x56":"0x56",
    "0x57":"0x57",
    "0x58":"0x58",
    "0x59":"0x59",
    "0x5A":"0x5A",
    "0x5B":"0x5B",
    "0x5C":"0x5C",
    "0x5D":"0x5D",
    "0x5F":"0x5F",
    "0x60":"0x60",
    "0x61":"0x61",
    "0x62":"0x62",
    "0x63":"0x63",
    "0x64":"0x64",
    "0x65":"0x65",
    "0x66":"0x66",
    "0x67":"0x67",
    "0x68":"0x68",
    "0x69":"0x69",
    "0x6A":"0x6A",
    "0x6B":"0x6B",
    "0x6C":"0x6C",
    "0x6D":"0x6D",
    "0x6E":"0x6E",
    "0x6F":"0x6F",
    "0x70":"0x70",
    "0x71":"0x71",
    "0x72":"0x72",
    "0x73":"0x73",
    "0x74":"0x74",
    "0x75":"0x75",
    "0x76":"0x76",
    "0x77":"0x77",
    "0x78":"0x78",
    "0x79":"0x79",
    "0x7A":"0x7A",
    "0x7B":"0x7B",
    "0x7C":"0x7C",
    "0x7D":"0x7D",
    "0x7E":"0x7E",
    "0x7F":"0x7F",
    "0x80":"0x80",
    "0x81":"0x81",
    "0x82":"0x82",
    "0x83":"0x83",
    "0x84":"0x84",
    "0x85":"0x85",
    "0x86":"0x86",
    "0x87":"0x87",
    "0x90":"0x90",
    "0x91":"0x91",
    "0xA0":"0xA0",
    "0xA1":"0xA1",
    "0xA2":"0xA2",
    "0xA3":"0xA3",
    "0xA4":"0xA4",
    "0xA5":"0xA5",
    "0xA6":"0xA6",
    "0xA7":"0xA7",
    "0xA8":"0xA8",
    "0xA9":"0xA9",
    "0xAA":"0xAA",
    "0xAB":"0xAB",
    "0xAC":"0xAC",
    "0xAD":"0xAD",
    "0xAE":"0xAE",
    "0xAF":"0xAF",
    "0xB0":"0xB0",
    "0xB1":"0xB1",
    "0xB2":"0xB2",
    "0xB3":"0xB3",
    "0xB4":"0xB4",
    "0xB5":"0xB5",
    "0xB6":"0xB6",
    "0xB7":"0xB7",
    "0xBA":"0xBA",
    "0xBB":"0xBB",
    "0xBC":"0xBC",
    "0xBD":"0xBD",
    "0xBE":"0xBE",
    "0xBF":"0xBF",
    "0xC0":"0xC0",
    "0xDB":"0xDB",
    "0xDC":"0xDC",
    "0xDD":"0xDD",
    "0xDE":"0xDE",
    "0xDF":"0xDF",
    "0xE2":"0xE2",
    "0xE5":"0xE5",
    "0xE7":"0xE7",
    "0xF6":"0xF6",
    "0xF7":"0xF7",
    "0xF8":"0xF8",
    "0xF9":"0xF9",
    "0xFA":"0xFA",
    "0xFB":"0xFB",
    "0xFD":"0xFD"
}

    asyncio.run(async_task())
    
    
    
