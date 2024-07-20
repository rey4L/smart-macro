import json
import os
import sys

def load_config():
    config_path = '..\src\config.json'
    if not os.path.exists(config_path):
        print("Config file not found. Please create a 'config.json' file.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return json.load(f)