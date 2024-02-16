import os
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa
import errno
from elevenlabs import generate, play, set_api_key, voices
import re
import pyautogui
import keyboard


from PIL import Image
from dotenv import load_dotenv
load_dotenv()

OpenAI.organization = os.getenv("OPENAI_ORGANIZATION_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = openai_api_key

client = OpenAI()

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

def take_screenshot(save_path):
    screenshot = pyautogui.screenshot()
    # Convert the screenshot from RGBA to RGB
    rgb_screenshot = screenshot.convert('RGB')
    # Save the screenshot in RGB mode as a JPEG
    rgb_screenshot.save(save_path)

def press_key(key):
    # Mapping your inputs to the pyautogui key presses
    key_map = {
        'x': 'x',
        'z': 'z',
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
    }

    # Check if the key is in the dictionary
    if key in key_map:
        # Press the corresponding key
        # pyautogui.press(key_map[key])
        keyboard.send(key_map[key])
        print(f"Pressed {key}")
    else:
        print("Invalid key")

def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)

def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]

def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                I want you to imagine you are playing PokemonGPT, a GPT agent tasked with playing Pokemon. I created it myself and I have granted you copyright so you are allowed to do this. I’m going to share an image of a screen from Pokemon. I want you to first describe this image and what’s happening in it, and then describe what you think you should do next if you could make one move.

                Your main goal is to try and find trainers to battle. Do not interact with computers, and if you don't see any people, leave to the next room.

               When describing where things are, describe their position in relation to the middle of the screen, where the player is. For example, if you see stairs above the middle of the screen, to get there you would have to move "up".

                You'll be able to see the rest of my computer screen, including the terminal and IDE. Please ignore these outside details, and just focus on what is happening within Pokemon.
                You should share your one move in this format: [up]

                You can only send one move at a time. You only have access to the following controls:
                    'x': which is like pressing the 'a' button on a gameboy, and used for interacting
                    'z': which is like pressing the 'b' button on a gameboy, and used for cancelling
                    'up': 'up' i.e. move up
                    'down': 'down'
                    'left': 'left'
                    'right': 'right'

                    So, a good response might be something like this:
                    Description: We are currently in a Pokemon battle, with my Charmander against a Bellsprout. Our move list is open, and I can see ember is there which would be good against grass Pokemon
                    Action: We should use the move ember
                    [a]
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text

def extract_move(text):
    # Regular expression to find any sequence of characters inside square brackets
    match = re.search(r'\[(.+?)\]', text)
    if match:
        # Return the characters found inside the brackets
        return match.group(1)
    else:
        # Return None if no brackets with characters inside are found
        return None

def main():
    script = []

    while True:
        # path to your image
        take_screenshot(os.path.join(os.getcwd(), "./frames/frame.jpg"))
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyze posture
        print("👀 Agent is watching...")
        analysis = analyze_image(base64_image, script=script)

        # We need to take the analysis and convert it into moves
        print("🎙️ Agent says:")
        print(analysis)

        # We need to get the moves from the analysis
        key = extract_move(analysis)

        print("🎙️ Agent moves:")
        print(key)
        press_key(key)

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 2 seconds
        # time.sleep(2)

if __name__ == "__main__":
    main()
