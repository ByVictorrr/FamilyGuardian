from reolinkapi import Camera

# Initialize the camera
camera_ip = "192.168.4.123"  # Replace with your camera's IP
username = "admin"           # Replace with your camera's username
password = "Sports22"        # Replace with your camera's password

camera = Camera(ip=camera_ip, username=username, password=password, verify=False)

# Test connection
if camera.login():
    print("Camera connected!")
else:
    print("Failed to connect to camera.")

# Capture a snapshot
snapshot_path = "snapshot.jpg"
snap_shot = camera.get_snap()
print(f"Snapshot saved at {snapshot_path}")
