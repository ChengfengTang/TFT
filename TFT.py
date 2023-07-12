import time
import numpy as np
import pytesseract
from PIL import Image
from mss import mss
import pyautogui
import pydirectinput
import concurrent.futures
import editdistance



class ThinkFast:
    def __init__(self, text):
        self.text = []
        self.temp = 0
        self.seen = []

    def process_region(self, i, screenshot_np):
        if i == 1:
            region = (480, 1030, 670, screen_height)
        elif i == 2:
            region = (680, 1030, 870, screen_height)
        elif i == 3:
            region = (880, 1030, 1070, screen_height)
        elif i == 4:
            region = (1080, 1030, 1270, screen_height)
        elif i == 5:
            region = (1280, 1030, 1470, screen_height)

        screenshot_np = screenshot_np[region[1]:region[3], region[0]:region[2]]
        screenshot = Image.fromarray(screenshot_np)
        screenshot = screenshot.resize((screenshot.size[0] * 5, screenshot.size[1] * 5))
        image_text = pytesseract.image_to_string((screenshot))
        temp = [x for x in  image_text.replace('\n', ' ').split(' ') if x.isalpha()]
        return (i, temp)

    def find_and_click_text(self):
        with mss() as sct:
            screenshot_np = np.array(sct.grab(sct.monitors[1]))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.process_region, range(1,6), [screenshot_np]*5))

        for i, temp in results:
            print(temp, end=' ')
            if any(text in temp for text in target_text):
                pydirectinput.PAUSE = 0.02
                pydirectinput.FAILSAFE = False
                pydirectinput.moveTo(420 + i * 200, 1000)
                pydirectinput.mouseDown()
                pydirectinput.mouseUp()
            time.sleep(0.02)
        time.sleep(0.15) #can change up to 0.35
        pydirectinput.moveTo(350, 1020)
        pydirectinput.mouseDown()
        pydirectinput.PAUSE = 0.1
        pydirectinput.mouseUp()
        time.sleep(0.02)
        # End timing


screen_width, screen_height = pyautogui.size()
target_text = ["Kayle", "Maokai", "Poppy", "PopPY"]
tf = ThinkFast(target_text)
while True:
    # Start timing here
    start_time = time.time()

    tf.find_and_click_text()

    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f'Time elapsed: {time_elapsed} seconds')