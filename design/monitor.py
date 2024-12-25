import time

def monitor():
    while True:
        # Step 1: Capture snapshot
        snapshot_path = "snapshot.jpg"
        camera.get_snapshot(snapshot_path)

        # Step 2: Process snapshot for face detection
        unknown_image = face_recognition.load_image_file(snapshot_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        for unknown_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
            if True in matches:
                match_index = matches.index(True)
                log_detection(known_face_names[match_index])
            else:
                log_detection()
                send_alert("recipient_email@example.com", snapshot_path)

        # Wait for a short interval before the next check
        time.sleep(10)

monitor()
