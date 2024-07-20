import cv2
import numpy as np
import mss
from PIL import Image
import pyautogui
import time

running = True

def signal_handler(sig, frame):
    global running
    print("\nCtrl+C detected. Stopping the script...")
    running = False

def wait_for_change(sct, original_screen, max_wait=10, check_interval=0.5):
    start_time = time.time()
    while time.time() - start_time < max_wait and running:
        new_screen = np.array(Image.frombytes('RGB', sct.grab(sct.monitors[1]).size, sct.grab(sct.monitors[1]).bgra, 'raw', 'BGRX'))
        if not np.array_equal(original_screen, new_screen):
            return True
        time.sleep(check_interval)
    return False

def load_templates(template_paths):
    templates = []
    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Error: Unable to load template {path}")
            continue
        templates.append((path, template))
    return templates

def template_matcher(template_paths, sensitivity):
    global running
    sct = mss.mss()
    print("Script is running. Press Ctrl+C to quit.")

    templates = load_templates(template_paths)

    while running:
        screen = sct.grab(sct.monitors[1])
        img = np.array(Image.frombytes('RGB', screen.size, screen.bgra, 'raw', 'BGRX'))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for template_path, template in templates:
            if not running:
                break
            w, h = template.shape[::-1] 
            result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            
            locations = np.where(result >= sensitivity)
            if np.any(locations):
                pt = list(zip(*locations[::-1]))[0]  # Get the first match
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                
                pyautogui.moveTo(center_x, center_y, duration=0.5)
                pyautogui.click()
                
                if not wait_for_change(sct, img):
                    print(f"No change detected after clicking {template_path}")
                
                break

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

    print("Script stopped.")