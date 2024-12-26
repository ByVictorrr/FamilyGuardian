# face_recognition.py

import face_recognition
import cv2
import os
import logging
from datetime import datetime
from config import RECORDINGS_DIR, ALERT_THRESHOLD

import os
import logging
import cv2
import face_recognition

def load_known_faces(known_people_dir):
    """
    Loads known faces and encodes them from the directory structure.

    Args:
        known_people_dir (str): Path to the root directory containing subdirectories for each person.

    Returns:
        list: Encoded face vectors.
        list: Corresponding names of individuals.
    """
    if not os.path.exists(known_people_dir):
        logging.warning(f"Directory {known_people_dir} does not exist. All faces will be treated as unknown.")
        return [], []

    known_face_encodings = []
    known_face_names = []

    for person_name, image_path in iterate_images(known_people_dir):
        face_encoding = process_image(image_path)
        if face_encoding is not None:
            known_face_encodings.append(face_encoding)
            known_face_names.append(person_name)
            logging.info(f"Loaded face for {person_name}: {os.path.basename(image_path)}")

    return known_face_encodings, known_face_names


def iterate_images(base_dir):
    """
    Generator to iterate through images in the directory structure.

    Args:
        base_dir (str): Base directory containing subdirectories for each person.

    Yields:
        tuple: Person's name and full path to an image file.
    """
    for person_name in os.listdir(base_dir):
        person_dir = os.path.join(base_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        image_dir = os.path.join(person_dir, "images")
        if not os.path.exists(image_dir):
            logging.warning(f"No 'images' directory found for {person_name}. Skipping...")
            continue

        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg', '.JPG')):
                yield person_name, os.path.join(image_dir, filename)


def process_image(image_path):
    """
    Process an image to detect and encode a face.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Encoded face vector if a face is found; otherwise, None.
    """
    try:
        image = face_recognition.load_image_file(image_path)
    except Exception as e:
        logging.warning(f"Error loading image {image_path}: {e}")
        return None

    if image is None or len(image.shape) != 3:
        logging.warning(f"Invalid image format: {image_path}. Skipping...")
        return None

    # Detect faces in the image
    face_locations = face_recognition.face_locations(image, model="cnn")
    if not face_locations:
        logging.warning(f"No faces found in {image_path}. Trying resized image...")
        image = resize_image(image, scale=0.5)
        face_locations = face_recognition.face_locations(image, model="cnn")

    if face_locations:
        encodings = face_recognition.face_encodings(image, face_locations)
        if encodings:
            return encodings[0]  # Use the first detected face encoding
        else:
            logging.warning(f"Unable to encode face in {image_path}.")
    else:
        logging.warning(f"No faces found in {image_path} after resizing.")
    return None


def resize_image(image, scale=0.5):
    """
    Resize an image by a given scale.

    Args:
        image (np.ndarray): Original image array.
        scale (float): Scaling factor.

    Returns:
        np.ndarray: Resized image array.
    """
    height, width = image.shape[:2]
    new_dimensions = (int(width * scale), int(height * scale))
    return cv2.resize(image, new_dimensions)






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
