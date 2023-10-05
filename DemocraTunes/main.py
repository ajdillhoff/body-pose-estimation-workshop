import cv2
import time

from vision import Vision

class DemocraTunes:
    def __init__(self):
        # Configurations
        self.vote_timeout = 1  # Seconds
        self.last_vote_time = time.time()

        self.cap = cv2.VideoCapture(0)  # Connect to the camera. Change 0 to 1 or 2 etc. if you have multiple cameras.
        self.vision = Vision(self.got_gesture)

    def got_gesture(self, gesture):
        time_since_last_vote = time.time() - self.last_vote_time

        if time_since_last_vote > self.vote_timeout:
            self.last_vote_time = time.time()
            print(gesture)

    def run(self):
        p_time = 0  # Previous time
        c_time = 0  # Current time

        print("Press 'q' to exit.")

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
            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # Display the frame
            cv2.imshow('Frame', frame)

            # Exit on pressing 'q'
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()



def main():
    app = DemocraTunes()
    app.run()

if __name__ == '__main__':
    main()