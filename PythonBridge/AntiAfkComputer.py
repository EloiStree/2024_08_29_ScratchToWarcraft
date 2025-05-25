import pyautogui
import random
import time

time_between_move=800
# Function to simulate pressing the space key
def press_key_to_interrupt_sleep_mode():
    pyautogui.keyDown('x')
    time.sleep(0.1)  # Adjust this duration as needed
    pyautogui.keyUp('x') 

    # pyautogui.keyDown('space')
    # time.sleep(0.1)  # Adjust this duration as needed
    # pyautogui.keyUp('space') 

# Function to move the mouse randomly on the screen
def move_mouse_randomly():
    screen_width, screen_height = pyautogui.size()
    new_x = random.randint(0, screen_width)
    new_y = random.randint(0, screen_height)
    pyautogui.moveTo(new_x, new_y, duration=0.5)

# Function to click at the center of the screen
def click_center():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.click(center_x, center_y)

# Main function to execute the actions
def main():
    try:
        while True:
            press_key_to_interrupt_sleep_mode()
            move_mouse_randomly()
            time.sleep(5)  # Wait for a second
            move_mouse_randomly()
            time.sleep(5)  # Wait for a second
            move_mouse_randomly()
            time.sleep(5)  # Wait for a second
            click_center()
            time.sleep(time_between_move)  # Wait for 60 seconds before repeating
            print (".")
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

if __name__ == "__main__":
    main()
