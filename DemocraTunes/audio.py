import time
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlayer:
    def __init__(self, callback, rate_limit=1):
        self.callback = callback
        self.previous_time = None
        self.should_shutdown = False
        self.rate_limit = rate_limit

        try:
            spotipy_client_id = os.environ["SPOTIPY_CLIENT_ID"]
            spotipy_client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
            spotipy_redirect_uri = os.environ["SPOTIPY_REDIRECT_URI", "http://localhost:8080"]
        except KeyError:
            print("Please set the SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI environment variables.")
            exit(1)

        # Initialize the Spotify API
        scope = "user-read-playback-state,user-modify-playback-state,streaming"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotipy_client_id, client_secret=spotipy_client_secret, redirect_uri=spotipy_redirect_uri, scope=scope))

        # Get the device ID
        self.device_id = None
        self.get_device_id()

    def get_device_id(self):
        """Attempts to connect a device if no device is connected."""
        try:
            devices = self.sp.devices()["devices"]
            self.device_id = devices[0]["id"]
        except IndexError:
            print("No device found. Please start Spotify on a device.")

    def update_status(self):
        """Get the status of the player."""

        if self.device_id is None:
            self.get_device_id()
            return

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
            time.sleep(self.rate_limit)

    def shutdown(self):
        print("Shutting down...")
        self.should_shutdown = True