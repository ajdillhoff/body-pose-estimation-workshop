import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Holistic()

cap = cv2.VideoCapture(0)  # Connect to the camera. Change 0 to 1 or 2 etc. if you have multiple cameras.

p_time = 0  # Previous time
c_time = 0  # Current time

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Process the frame
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(image_rgb)

    # Draw pose landmarks
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks
    mp_drawing.draw_landmarks(image_rgb, result.left_hand_landmarks, mp_pose.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image_rgb, result.right_hand_landmarks, mp_pose.HAND_CONNECTIONS)

    # Draw pose landmarks
    mp_drawing.draw_landmarks(image_rgb, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Calculate and display FPS
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(image_rgb, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Display the frame
    cv2.imshow('Frame', image_rgb)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
