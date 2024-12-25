import cv2
import numpy as np
import mediapipe as mp
from reolinkapi import Camera
import face_recognition
import os
from datetime import datetime
from

class ReolinkFaceRecognition:
    def __init__(self, ip, username, password, port=80):
        self.camera = Camera(
            host=ip,
            username=username,
            password=password,
            port=port
        )
        self.known_faces_encodings = []
        self.known_faces_names = []
        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    def load_known_faces(self, known_faces_dir="known_faces"):
        """
        Load known faces from a directory.
        :param known_faces_dir: Directory containing known face images.
        """
        for file in os.listdir(known_faces_dir):
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(known_faces_dir, file)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_faces_encodings.append(encodings[0])
                    self.known_faces_names.append(file.split('.')[0])

    def start_stream(self):
        """
        Start the stream from the Reolink camera and process frames.
        """
        try:
            stream_url = self.camera.get_rtsp_url(stream="main")
            cap = cv2.VideoCapture(stream_url)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame from stream.")
                    break

                # Convert the frame to RGB for face recognition
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect faces in the frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding, face_location in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(self.known_faces_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        match_index = matches.index(True)
                        name = self.known_faces_names[match_index]

                    # If the face is unknown, save the snapshot and alert
                    if name == "Unknown":
                        self.alert(frame, face_location)

                # Display the frame (optional)
                cv2.imshow("Reolink Stream", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Error: {e}")

    def alert(self, frame, face_location):
        """
        Save the snapshot of an unknown face and trigger an alert.
        :param frame: The video frame.
        :param face_location: Location of the face in the frame.
        """
        top, right, bottom, left = face_location
        face_image = frame[top:bottom, left:right]

        # Save the face image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alerts/unknown_{timestamp}.jpg"
        os.makedirs("alerts", exist_ok=True)
        cv2.imwrite(filename, face_image)

        print(f"Alert: Unknown face detected and saved to {filename}")


# Main Function
if __name__ == "__main__":
    # Initialize the system
    ip = "192.168.1.100"  # Replace with your camera's IP
    username = "admin"    # Replace with your camera's username
    password = "password" # Replace with your camera's password

    face_recognition_system = ReolinkFaceRecognition(ip, username, password)
    face_recognition_system.load_known_faces()
    face_recognition_system.start_stream()
