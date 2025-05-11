import ctypes
from ctypes import wintypes
import time
import sys

bool_10_second_ninja_config = False
if bool_10_second_ninja_config:
    window_exact_name = "10 Second Ninja"
    bool_use_stretch = True

bool_world_of_warcraft_config = True
if bool_world_of_warcraft_config:
    window_exact_name = "World of Warcraft"
    bool_use_stretch = True

if len(sys.argv) > 1:
    window_exact_name = sys.argv[1]

# Get user32 functions
user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible
MoveWindow = user32.MoveWindow
GetWindowRect = user32.GetWindowRect

hwnd_list = []

def foreach_window_display(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if buff.value == window_exact_name:
            hwnd_list.append(hwnd)

# Enumerate all windows and apply foreach_window function
EnumWindows(EnumWindowsProc(foreach_window_display), 0)

print("Displaying hwnds")   
for t in hwnd_list:
    print(t)

# Get screen dimensions
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

gamecount = len(hwnd_list)
columns = 4  # Fixed number of columns
if len(hwnd_list) == 1:
    columns = 1
elif len(hwnd_list) <= 4:
    columns = 2
elif len(hwnd_list) <= 9:
    columns = 4
else:
    columns = 4

if len(hwnd_list) ==6:
    columns = 3


# Calculate number of rows dynamically based on the total number of windows and columns
rows = (gamecount + columns - 1) // columns  # Calculate the number of rows needed

# Position counters for windows
current_column = 0
current_row = 0

def foreach_window(hwnd, lParam):
    global current_column, current_row
    global bool_use_stretch

    # Check if the window is visible
    if IsWindowVisible(hwnd):
        # Get the length of the window's title
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        # Get the window's title
        GetWindowText(hwnd, buff, length + 1)

        # Check if the window title is window_exact_name
        if buff.value == window_exact_name:
            # Make the window visible and bring it to the foreground
            time.sleep(0.1)
            user32.ShowWindow(hwnd, 5)  # 5 = SW_SHOW
            time.sleep(0.1)
            user32.SetForegroundWindow(hwnd)
            if bool_use_stretch:
                # Calculate the width and height for each window in the grid
                window_width = screen_width // columns
                window_height = screen_height // rows

                # Calculate the position for the current window in the grid
                x = current_column * window_width
                y = current_row * window_height

                # Move the window to the calculated position and size
                MoveWindow(hwnd, x, y, window_width, window_height, True)
            else:
                # Get the original size of the window
                rect = wintypes.RECT()
                GetWindowRect(hwnd, ctypes.byref(rect))
                window_width = rect.right - rect.left
                window_height = rect.bottom - rect.top

                # Calculate the position for the current window in the grid
                x = current_column * window_width
                y = current_row * window_height

                # Move the window to the calculated position
                MoveWindow(hwnd, x, y, window_width, window_height, True)

            # Update position counters
            current_column += 1
            if current_column >= columns:
                current_column = 0
                current_row += 1
                # Stop if all windows are placed
                if current_row >= rows:
                    return False  # Stop enumerating after placing all windows

    return True

# Enumerate all windows and apply foreach_window function
EnumWindows(EnumWindowsProc(foreach_window), 0)
