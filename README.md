# Configuration file for Family Guardian

# Reolink camera settings
CAMERA_IP = 'http://<camera_ip>'
USERNAME = 'your_username'
PASSWORD = 'your_password'

# Directory paths
KNOWN_PEOPLE_DIR = 'data/known_people/'
RECORDINGS_DIR = 'data/recordings/'

# Other settings
PROCESS_FRAME_INTERVAL = 1  # Process every nth frame
ALERT_THRESHOLD = 15  # Seconds an unknown person must be in view to trigger alert
