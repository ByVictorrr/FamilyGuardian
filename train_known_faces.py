import os
import logging
import face_recognition
import pickle


def train_known_faces(known_people_dir, output_file="encodings.pkl"):
    """
    Encodes known faces from the directory and saves them to a file.

    Args:
        known_people_dir (str): Path to the directory containing subdirectories for each person.
        output_file (str): File to save the encodings and names.
    """
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(known_people_dir):
        logging.error(f"Directory {known_people_dir} does not exist.")
        return

    for person_name in os.listdir(known_people_dir):
        person_dir = os.path.join(known_people_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        image_dir = os.path.join(person_dir, "images")
        if not os.path.exists(image_dir):
            logging.warning(f"No 'images' directory found for {person_name}. Skipping...")
            continue

        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(image_dir, filename)
                image = face_recognition.load_image_file(image_path)

                # Detect faces and encode them
                face_locations = face_recognition.face_locations(image, model="cnn")
                encodings = face_recognition.face_encodings(image, face_locations)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(person_name)
                    logging.info(f"Encoded face for {person_name}: {filename}")
                else:
                    logging.warning(f"No faces found or unable to encode in {image_path}. Skipping...")

    # Save encodings to file
    with open(output_file, "wb") as f:
        pickle.dump({"encodings": known_face_encodings, "names": known_face_names}, f)
    logging.info(f"Encodings saved to {output_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    KNOWN_PEOPLE_DIR = "data"  # Path to known faces directory
    OUTPUT_FILE = "encodings.pkl"  # File to save encodings

    train_known_faces(KNOWN_PEOPLE_DIR, OUTPUT_FILE)
