import os
import logging
import face_recognition
import pickle
from PIL import Image, ImageEnhance
import random


def augment_image(image):
    """
    Applies random augmentations to the given image.

    Args:
        image (PIL.Image.Image): The input image.

    Returns:
        list: A list of augmented images.
    """
    augmented_images = []

    # Original image
    augmented_images.append(image)

    # Flip horizontally
    augmented_images.append(image.transpose(Image.FLIP_LEFT_RIGHT))

    # Rotate slightly
    angles = [-15, -10, -5, 5, 10, 15]
    for angle in angles:
        augmented_images.append(image.rotate(angle))

    # Brightness adjustment
    enhancer = ImageEnhance.Brightness(image)
    for factor in [0.8, 1.2]:  # Darker and brighter
        augmented_images.append(enhancer.enhance(factor))

    # Add Gaussian blur (simulate motion blur)
    blurred = image.filter(ImageFilter.GaussianBlur(radius=2))
    augmented_images.append(blurred)

    return augmented_images


def train_known_faces(known_faces_dir, output_file="encodings.pkl"):
    """
    Encodes known faces from the directory, applies augmentation, and saves them to a file.

    Args:
        known_faces_dir (str): Path to the directory containing subdirectories for each person.
        output_file (str): File to save the encodings and names.
    """
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(known_faces_dir):
        logging.error(f"Directory {known_faces_dir} does not exist.")
        return

    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        for filename in os.listdir(person_dir):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(person_dir, filename)
                if not os.path.isfile(image_path):
                    logging.warning(f"Invalid file path: {image_path}. Skipping...")
                    continue

                try:
                    # Load the image
                    image = Image.open(image_path)

                    # Augment the image
                    augmented_images = augment_image(image)

                    # Process each augmented image
                    for augmented_image in augmented_images:
                        augmented_image = augmented_image.convert("RGB")  # Ensure RGB format
                        image_array = face_recognition.load_image_file(augmented_image)
                        face_locations = face_recognition.face_locations(image_array, model="cnn")
                        encodings = face_recognition.face_encodings(image_array, face_locations)

                        if encodings:
                            known_face_encodings.append(encodings[0])
                            known_face_names.append(person_name)
                            logging.info(f"Encoded face for {person_name}: {filename} (augmented)")
                        else:
                            logging.warning(f"No faces found or unable to encode in {image_path}. Skipping...")
                except Exception as e:
                    logging.error(f"Error processing {image_path}: {str(e)}")

    # Save encodings to file
    with open(output_file, "wb") as f:
        pickle.dump({"encodings": known_face_encodings, "names": known_face_names}, f)
    logging.info(f"Encodings saved to {output_file}")


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Train known faces and save encodings.")
    parser.add_argument("--known-faces-dir", type=str, help="Path to the directory containing known faces.")
    parser.add_argument("--output-file", type=str, default="encodings.pkl", help="Output file to save encodings.")
    args = parser.parse_args()

    train_known_faces(args.known_faces_dir, args.output_file)
