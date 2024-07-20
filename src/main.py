import signal
from config import load_config
from image_processing import template_matcher, signal_handler

def main():
    signal.signal(signal.SIGINT, signal_handler)

    config = load_config()
    templates = config['templates']
    sensitivity = config.get('sensitivity', 0.8)  # Default sensitivity if not specified
    
    template_matcher(templates, sensitivity)

if __name__ == "__main__":
    main()