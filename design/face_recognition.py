import face_recognition

# Load known faces
known_face_encodings = []
known_face_names = ["Alice", "Bob", "Charlie"]

for name in known_face_names:
    image_path = f"family/{name}.jpg"  # Replace with the folder where you store known faces
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)

# Load an unknown image
unknown_image_path = "snapshot.jpg"
unknown_image = face_recognition.load_image_file(unknown_image_path)

# Find faces in the unknown image
unknown_face_encodings = face_recognition.face_encodings(unknown_image)
for unknown_encoding in unknown_face_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
    if True in matches:
        match_index = matches.index(True)
        print(f"Recognized: {known_face_names[match_index]}")
    else:
        print("Unrecognized face detected!")
