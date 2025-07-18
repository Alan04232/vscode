import cv2
import numpy as np

# Start capturing from the default webcam (0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("❌ Error: Cannot open webcam.")
    exit()

print("🚀 Running ESP32-CAM Navigation Simulation (Press 'q' to exit)")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Failed to grab frame.")
        break

    # Resize frame for performance
    frame = cv2.resize(frame, (640, 480))

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold to find dark areas (simulate obstacles)
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Default message
    direction = "Path Clear ✅"

    # Analyze each detected contour
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # Ignore small objects
            # Get bounding box of the obstacle
            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w / 2  # Center x of the box

            # Draw rectangle around the obstacle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Decide direction based on obstacle position
            if cx < 213:
                direction = "⚠️ Obstacle Left"
            elif cx > 426:
                direction = "⚠️ Obstacle Right"
            else:
                direction = "🛑 Obstacle Ahead"

            # Stop checking after first large obstacle
            break

    # Overlay the decision text on the video
    cv2.putText(frame, f"Direction: {direction}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if direction == "Path Clear ✅" else (0, 0, 255), 2)

    # Show the final video feed
    cv2.imshow("ESP32-CAM Navigation Simulation", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Simulation Ended.")
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
