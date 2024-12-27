import os
import cv2
import logging
from datetime import datetime
import pickle
import face_recognition
from dotenv import load_dotenv
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# Load environment variables from .env file
load_dotenv()

CAMERA_IP = os.getenv("CAMERA_IP")
CAMERA_USER = os.getenv("CAMERA_USER")
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD")

PROCESS_FRAME_INTERVAL = int(os.getenv("PROCESS_FRAME_INTERVAL"))
# Directory to save recordings
RECORDINGS_DIR = os.getenv('RECORDINGS_DIR', 'recordings')  # Default to 'recordings' if not specified

# Alert threshold in seconds
ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 15))  # Default to 15 seconds if not specified
################### SMS Video alert ######################
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")
PHONE_CARRIER_GATEWAY = os.getenv("PHONE_NUMBER_CARRIER_GATEWAY")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_SERVER= os.getenv("SMTP_SERVER")


def load_known_faces(pkl_file_path):
    """Loads known faces and names from a pickle file.

    :returns tuple: List of encoded face vectors, corresponding names of individuals.
    """
    if not os.path.exists(pkl_file_path):
        logging.warning(f"Pickle file {pkl_file_path} does not exist. All faces will be treated as unknown.")
        return [], []

    try:
        with open(pkl_file_path, "rb") as f:
            data = pickle.load(f)
            return data.get("encodings", []), data.get("names", [])
    except Exception as e:
        logging.error(f"Failed to load pickle file {pkl_file_path}: {e}")
        return [], []


def initialize_video_stream(rtsp_url):
    """
    Initializes the video stream from the given RTSP URL.

    Args:
        rtsp_url (str): RTSP URL of the video stream.

    Returns:
        cv2.VideoCapture: Opened video capture object.
    """
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise ValueError("Unable to open video stream.")
        logging.info("Opened video stream from RTSP URL.")
        return cap
    except Exception as e:
        logging.error(f"Failed to open video stream: {e}")
        raise


def handle_unknown_face(unknown_frames, unknown_face_start_time):
    """
    Handles the unknown face detection, saves the recording, and triggers an alert.

    Args:
        unknown_frames (list): List of frames containing the unknown face.
        unknown_face_start_time (datetime): Time when the unknown face was first detected.

    Returns:
        tuple: Updated unknown face start time and unknown frames list.
    """
    duration = (datetime.now() - unknown_face_start_time).total_seconds()
    if duration > ALERT_THRESHOLD:
        video_path = save_recording(unknown_frames)
        logging.info(f"Unknown face recorded and saved to: {video_path}")
        # TODO: Add notification or alert system
        return None, []
    return unknown_face_start_time, unknown_frames


def send_video_to_phone(video_file_path, smtp_port=587):
    """Sends a video file to a phone number via an MMS gateway."""
    if not os.path.exists(video_file_path):
        print(f"Error: Video file {video_file_path} does not exist.")
        return

    # Create the email
    recipient = f"{TO_PHONE_NUMBER}@{PHONE_CARRIER_GATEWAY}"
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = recipient
    msg["Subject"] = "Video Attachment"  # Optional; may not appear on all devices

    # Attach the video file
    with open(video_file_path, "rb") as video_file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(video_file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(video_file_path)}",
        )
        msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, smtp_port) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
            print(f"Video sent to {recipient}")
    except Exception as e:
        print(f"Failed to send MMS: {e}")



def process_video_frames(cap_obj: cv2.VideoCapture, known_face_encodings, known_face_names, process_frame_interval=1):
    """Processes video frames, detects and identifies faces, and handles unknown faces."""
    frame_count = 0
    unknown_face_start_time = None
    unknown_frames = []

    while cap_obj.isOpened():
        ret, frame = cap_obj.read()
        if not ret:
            logging.error("Failed to capture frame. Exiting...")
            break

        if frame_count % process_frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                if name == "Unknown":
                    if unknown_face_start_time is None:
                        unknown_face_start_time = datetime.now()
                        unknown_frames = [frame]
                    else:
                        unknown_face_start_time, unknown_frames = handle_unknown_face(
                            unknown_frames, unknown_face_start_time
                        )
                        unknown_frames.append(frame)
                else:
                    unknown_face_start_time = None
                    unknown_frames = []

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        frame_count += 1

    cap_obj.release()
    cv2.destroyAllWindows()


def save_recording(frames, fps=20.0):
    """
    Saves the given frames as a video recording.

    Args:
        frames (list): List of frames to save.
        fps (float): Frames per second for the recording.

    Returns:
        str: Path to the saved video file.
    """
    if not frames:
        raise ValueError("No frames to save.")

    os.makedirs("recordings", exist_ok=True)

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join("recordings", f"recording_{timestamp}.mp4")
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    return video_path


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Family Guardian application.")

    # Load known faces
    _known_face_encodings, _known_face_names = load_known_faces("encoding/encodings.pkl")

    # Initialize video stream
    rtsp_url = f"rtsp://{CAMERA_USER}:{CAMERA_PASSWORD}@{CAMERA_IP}:554/h264Preview_01_main"
    cap = initialize_video_stream(rtsp_url)

    # Process video frames
    process_video_frames(cap, _known_face_encodings, _known_face_names, PROCESS_FRAME_INTERVAL)

    logging.info("Family Guardian application has stopped.")
