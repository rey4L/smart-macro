import json
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__)) # Adapted from https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory

def load_config():
    config_path = os.path.join(pwd, 'config.json')
    if not os.path.exists(config_path):
        print("Config file not found. Please create a 'config.json' file.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return json.load(f)