# face_recognition.py

import face_recognition
import cv2
import os
import logging
from datetime import datetime
from config import RECORDINGS_DIR, ALERT_THRESHOLD


def load_known_faces(known_people_dir):
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(known_people_dir):
        logging.warning(f"Directory {known_people_dir} does not exist. All faces will be treated as unknown.")
        return known_face_encodings, known_face_names

    for filename in os.listdir(known_people_dir):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(known_people_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
                logging.info(f"Loaded known face: {filename}")
            else:
                logging.warning(f"No face found in {image_path}. Skipping this file.")

    return known_face_encodings, known_face_names


def save_recording(frames, fps=20.0):
    if not frames:
        raise ValueError("No frames to save.")

    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.mp4")
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    return video_path


def process_video_frames(cap, known_face_encodings, known_face_names, process_frame_interval=1):
    frame_count = 0
    unknown_face_start_time = None
    unknown_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
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
                        duration = (datetime.now() - unknown_face_start_time).total_seconds()
                        unknown_frames.append(frame)
                        if duration > ALERT_THRESHOLD:
                            video_path = save_recording(unknown_frames)
                            # Implement notification and response handling here
                            unknown_face_start_time = None
                            unknown_frames = []
                else:
                    unknown_face_start_time = None
                    unknown_frames = []

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
