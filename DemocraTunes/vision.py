import cv2
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp

class Vision:
    def __init__(self, callback):
        self.callback = callback

        # Get the path of the model
        current_dir = Path(__file__)
        models_dir = current_dir.parent.parent / "models"
        model_path = str(models_dir / "gesture_recognizer.task")

        base_options = python.BaseOptions(model_asset_path=model_path)
        running_mode = vision.RunningMode.LIVE_STREAM
        options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=running_mode, result_callback=self.result_callback)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def result_callback(self, result: vision.GestureRecognizerResult, output_image: mp.Image, frame_timestamp: int):
        """Callback function that will be called when the gesture recognizer has a result."""

        if len(result.gestures) == 0:
            return

        if result.gestures[0][0].category_name == "Thumb_Down":
            self.callback("downvote")
        elif result.gestures[0][0].category_name == "Thumb_Up":
            self.callback("upvote")

    def process_frame(self, frame):
        """Process a frame (opencv image) and return the result with landmarks."""

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        frame_timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

        self.recognizer.recognize_async(mp_image, frame_timestamp_ms)