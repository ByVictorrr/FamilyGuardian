import cv2
import face_recognition
import time

# Start the video stream
stream_url = camera.rtsp_url  # Obtain the RTSP URL from the camera
video_capture = cv2.VideoCapture(stream_url)

# Load known faces
known_face_encodings = []
known_face_names = []

# Load images from the data directory
# (Assuming you have a directory named 'data' with images of known individuals)
import os
for filename in os.listdir('data'):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image = face_recognition.load_image_file(f'data/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

# Function to send email alerts
def send_email_alert(image_path):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_email_password"

    subject = "Family Guard Alert: Unknown Person Detected"
    body = "An unknown person was detected. Please review the attached image."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(image_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
    msg.attach(part)

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Main loop
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        if name == "Unknown":
            # Save the frame as an image file
            timestamp = int(time.time())
            image_path = f'unknown_{timestamp}.jpg'
            cv2.imwrite(image_path, frame)

            # Send an email alert with the image attached
            send_email_alert(image_path)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()

# Main
if __name__ == "__main__":
    # Initialize the camera
    camera_ip = "192.168.4.123"  # Replace with your camera's IP
    username = "admin"  # Replace with your camera's username
    password = "Sports22"  # Replace with your camera's password

    guard = FamilyGuard(camera_ip, username, password)
    guard.train_model()
    guard.monitor()
