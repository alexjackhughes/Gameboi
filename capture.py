import os
import time
from PIL import Image
import numpy as np
import cv2
import pyautogui

# Folder
folder = "frames"

# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)

while True:
    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a PIL image
    pil_img = Image.fromarray(np.array(screenshot))

    # Resize the image
    max_size = 250
    ratio = max_size / max(pil_img.size)
    new_size = tuple([int(x*ratio) for x in pil_img.size])
    resized_img = pil_img.resize(new_size, Image.LANCZOS)

    # Convert the PIL image back to an OpenCV image
    frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

    # Save the frame as an image file
    print("📸 Snapshot taken! Saving frame.")
    path = f"{folder}/frame.jpg"
    cv2.imwrite(path, frame)

    # Wait for 2 seconds
    time.sleep(2)