import cv2


class FaceDetector:
    def __init__(self, model_path=None):
        """
        Initialize the FaceDetector class.

        :param model_path: Path to the Haar Cascade model file. Defaults to OpenCV's built-in model.
        """
        if model_path is None:
            model_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(model_path)

    def contains_face(self, image_path):
        """
        Check if an image contains a face.

        :param image_path: Path to the image file.
        :return: True if a face is detected, False otherwise.
        """
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from path: {image_path}")

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        return len(faces) > 0

    def process_frame(self, frame):
        """
        Check if a live frame from a video feed contains a face.

        :param frame: Frame (image) from a video feed or camera.
        :return: True if a face is detected, False otherwise.
        """
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces) > 0
