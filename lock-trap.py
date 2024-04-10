import subprocess
from pynput.mouse import Listener
from datetime import datetime
import os
import cv2
import tempfile
import time
import sys

# Global variables to store the previous mouse position and last trigger time
prev_x, prev_y = 0, 0
last_trigger_time = datetime.now()

# Threshold distance for triggering the event
threshold_distance = 10  # Adjust this value as needed
cooldown_duration = 5  # Adjust this value (in seconds) as needed

def calculate_distance(x1, y1, x2, y2):
    # Calculate Euclidean distance between two points
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def on_move(x, y):
    global prev_x, prev_y, last_trigger_time

    # Calculate distance from the previous position
    distance_moved = calculate_distance(prev_x, prev_y, x, y)

    # Check if the distance moved is greater than the threshold and cooldown period has passed
    if distance_moved > threshold_distance and (datetime.now() - last_trigger_time).total_seconds() > cooldown_duration:
        print(f'Mouse moved to ({x}, {y})')

        # Update the last trigger time
        last_trigger_time = datetime.now()

        # Play the camera click audio
        os.system(f'open iphone-camera-capture-6448.mp3')

        # Capture a camera snapshot
        capture_camera_snapshot()
        # time.sleep(1)
        subprocess.run(['say', 'Nice try, champ!'])
        # time.sleep(1)

        # Play the camera click audio
        os.system(f'open sarcastic-villain-laugh_02-109108.mp3')

        # Sleep for 5 seconds
        time.sleep(5)

        # Lock the screen
        os.system("osascript -e 'tell application \"System Events\" to keystroke \"q\" using {command down, control down}'")

        # Terminate the script
        sys.exit()

    # Update the previous mouse position
    prev_x, prev_y = x, y

def capture_camera_snapshot():
    # Open the default camera (usually the webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Unable to read frame.")
        return

    # Release the camera
    cap.release()

    # Get the temporary directory path
    temp_dir = tempfile.gettempdir()

    # Generate a unique filename for the snapshot based on current timestamp
    filename = os.path.join(temp_dir, f"snapshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
    # Generate a unique filename for the snapshot based on current timestamp
    # filename = f"snapshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

    # Save the captured frame to disk
    cv2.imwrite(filename, frame)
    print(f"Snapshot saved as {filename}")

    # Open the saved image file with the default image viewer
    os.system(f'open {filename}')

# Set up the listener
with Listener(on_move=on_move) as listener:
    # Run the listener in the background
    listener.join()
