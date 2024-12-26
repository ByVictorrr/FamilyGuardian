# main.py

import logging
import cv2
from face_recognization import load_known_faces, process_video_frames
from config import CAMERA_IP, CAMERA_USER, CAMERA_PASSWORD, KNOWN_PEOPLE_DIR, PROCESS_FRAME_INTERVAL


def open_rtsp_stream(rtsp_url):
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise ValueError("Unable to open video stream.")
        logging.info("Opened video stream from RTSP URL.")
        return cap
    except Exception as e:
        logging.error(f"Failed to open video stream: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Family Guardian application.")

    known_face_encodings, known_face_names = load_known_faces(KNOWN_PEOPLE_DIR)

    rtsp_url = f"rtsp://{CAMERA_USER}:{CAMERA_PASSWORD}@{CAMERA_IP}:554/h264Preview_01_main"
    cap = open_rtsp_stream(rtsp_url)

    process_video_frames(cap, known_face_encodings, known_face_names, PROCESS_FRAME_INTERVAL)

    logging.info("Family Guardian application has stopped.")
