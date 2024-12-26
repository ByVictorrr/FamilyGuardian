import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
CAMERA_IP = os.getenv("CAMERA_IP")
CAMERA_USER = os.getenv("CAMERA_USER")
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD")
KNOWN_PEOPLE_DIR = os.getenv("KNOWN_PEOPLE_DIR", "data")
PROCESS_FRAME_INTERVAL = int(os.getenv("PROCESS_FRAME_INTERVAL"))
# CAMERA_IP, USERNAME, PASSWORD, KNOWN_PEOPLE_DIR, PROCESS_FRAME_INTERVAL
# Directory to save recordings
RECORDINGS_DIR = os.getenv('RECORDINGS_DIR', 'recordings')  # Default to 'recordings' if not specified

# Alert threshold in seconds
ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 15))  # Default to 15 seconds if not specified