from argparse import Namespace
import json
from pathlib import Path
import cv2
import time
from threading import Thread

from vision import Vision
from audio import SpotifyPlayer

class Track:
    def __init__(self, track_info):
        self.id = track_info["item"]["id"]
        self.name = track_info["item"]["name"]
        self.artist = track_info["item"]["artists"][0]["name"]
        self.album = track_info["item"]["album"]["name"]
        self.upvotes = 0
        self.downvotes = 0

    def __eq__(self, other):
        return self.id == other.id

class DemocraTunes:
    def __init__(self, params):
        # Configurations
        self.last_vote_time = time.time()
        self.log = []
        self.current_track = None
        self.vote_timeout = params.vote_timeout  # Seconds
        self.vote_threshold = params.vote_threshold  # This is the difference between upvotes and downvotes that is required to skip a song

        # Initialize the camera and vision system
        self.cap = cv2.VideoCapture(0)  # Connect to the camera. Change 0 to 1 or 2 etc. if you have multiple cameras.

        # Set the camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, params.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, params.height)

        self.cap.set(cv2.CAP_PROP_FPS, params.fps)  # Needed to work with OSX
        self.vision = Vision(self.got_gesture, params.gesture_model)

        # Initialize the player
        self.player = SpotifyPlayer(self.audio_status_callback, params.rate_limit)
        self.player_thread = Thread(target=self.player.run)

    def got_gesture(self, gesture):
        """Callback for when a gesture is detected."""
        time_since_last_vote = time.time() - self.last_vote_time

        if time_since_last_vote > self.vote_timeout:
            self.last_vote_time = time.time()
            
            if self.current_track is not None:
                if gesture == "upvote":
                    self.current_track.upvotes += 1
                    print(f"Upvoted {self.current_track.name} by {self.current_track.artist} from {self.current_track.album}")
                elif gesture == "downvote":
                    self.current_track.downvotes += 1
                    print(f"Downvoted {self.current_track.name} by {self.current_track.artist} from {self.current_track.album}")

                if self.current_track.downvotes - self.current_track.upvotes >= self.vote_threshold:
                    print(f"Skipping {self.current_track.name} by {self.current_track.artist} from {self.current_track.album}")
                    self.player.sp.next_track()

    def audio_status_callback(self, track_info):
        """Callback for when the audio status is updated."""

        # Create a track object
        track = Track(track_info)

        # Check if the track is the same as the current track
        if self.current_track is None or self.current_track != track:
            self.current_track = track
            self.log.append(track)
            print(f"Now playing: {track.name} by {track.artist} from {track.album}")

    def display_track_info(self, frame):
        """Displays the track info on the screen."""

        if self.current_track is None:
            return

        overlay = frame.copy()

        # Get bottom of the screen
        height, _, _ = overlay.shape

        # Get the size of the longest string
        longest_string = max("Title: " + self.current_track.name, "Artist: " + self.current_track.artist, "Album: " + self.current_track.album, key=len)
        text_width, _ = cv2.getTextSize(longest_string, cv2.QT_FONT_NORMAL, 0.6, 1)[0]

        # Create a transparent rectangle that the text will sit on
        cv2.rectangle(overlay, (0, height - 130), (text_width + 20, height), (0, 0, 0, 100), -1)

        # Add the overlay to the frame
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

        # Display the text
        cv2.putText(frame, f"Title: {self.current_track.name}", (10, height - 100), cv2.QT_FONT_NORMAL, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Artist: {self.current_track.artist}", (10, height - 80), cv2.QT_FONT_NORMAL, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Album: {self.current_track.album}", (10, height - 60), cv2.QT_FONT_NORMAL, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Upvotes: {self.current_track.upvotes}", (10, height - 40), cv2.QT_FONT_NORMAL, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Downvotes: {self.current_track.downvotes}", (10, height - 20), cv2.QT_FONT_NORMAL, 0.6, (255, 255, 255), 1)

    def run(self):
        p_time = 0  # Previous time
        c_time = 0  # Current time

        print("Press 'q' to exit.")

        # Start the player thread
        self.player_thread.start()

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Process the frame
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get the gesture
            self.vision.process_frame(image_rgb)

            # Calculate and display FPS
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            cv2.putText(frame, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # Display the track info
            self.display_track_info(frame)

            # Display the frame
            cv2.imshow('Frame', frame)

            # Exit on pressing 'q'
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

        # Shutdown player
        self.player.shutdown()
        self.player_thread.join()


def main():
    params = Namespace(**json.load(open((Path(__file__).parent / "config.json"), "r")))
    app = DemocraTunes(params)
    app.run()

if __name__ == '__main__':
    main()