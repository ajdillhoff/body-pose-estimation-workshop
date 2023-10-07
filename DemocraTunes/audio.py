import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT = "dbdeb55d09944707bf984d5d08b2ebd7"
SPOTIPY_SECRET = "690c13f9fa7c47d69c130cc8e74914f2"
SPOTIPY_REDIRECT_URI = "http://localhost:8080"

class SpotifyPlayer:
    RATE_LIMIT = 1  # Seconds

    def __init__(self, callback):
        self.callback = callback
        self.previous_time = None
        self.should_shutdown = False

        # Initialize the Spotify API
        scope = "user-read-playback-state,user-modify-playback-state,streaming"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT, client_secret=SPOTIPY_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))

        # Get the device ID
        devices = self.sp.devices()["devices"]
        self.device_id = devices[0]["id"]

        self.history = []
        self.current_status = []

    def update_status(self):
        """Get the status of the player."""

        track_info = self.sp.currently_playing()
        if track_info is None:
            return
        
        # get progress
        progress = track_info["progress_ms"]

        if self.previous_time is None:
            self.previous_time = progress
            return
        
        if self.previous_time == progress:
            return
        
        self.callback(track_info)

    def run(self):
        """Run the player."""

        while self.should_shutdown is False:
            self.update_status()
            time.sleep(self.RATE_LIMIT)

    def shutdown(self):
        print("Shutting down...")
        self.should_shutdown = True