import cv2
import numpy as np

def detect_direction(frame):
    # Resize for consistency
    frame = cv2.resize(frame, (640, 480))

    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    # Threshold to highlight dark areas
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Split frame into 3 vertical sections: left, center, right
    h, w = thresh.shape
    left = thresh[:, :w//3]
    center = thresh[:, w//3:2*w//3]
    right = thresh[:, 2*w//3:]

    # Count white pixels (simulating obstacles)
    counts = [np.sum(zone == 255) for zone in [left, center, right]]

    # Decide direction
    if max(counts) < 500:
        print ("Go Straight")
        return "Go Straight"
    elif counts[1] > counts[0] and counts[1] > counts[2]:
        print ("stop")
        return "Stop"
    elif counts[0] > counts[2]:
        print ("Turn Right")
        return "Turn Right"
    else:
        print ("Turn Left")
        return "Turn Left"

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("📷 Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    direction = detect_direction(frame)

    # Draw guide lanes
    h, w = frame.shape[:2]
    center_x = w // 2

    # Draw 3 vertical zones
    cv2.line(frame, (w//3, 0), (w//3, h), (255, 255, 255), 1)
    cv2.line(frame, (2*w//3, 0), (2*w//3, h), (255, 255, 255), 1)

    # Draw direction arrow
    if direction == "Go Straight":
        cv2.arrowedLine(frame, (center_x, h), (center_x, h//2), (0, 255, 0), 5)
    elif direction == "Turn Left":
        cv2.arrowedLine(frame, (center_x, h), (center_x - 100, h//2), (0, 255, 255), 5)
    elif direction == "Turn Right":
        cv2.arrowedLine(frame, (center_x, h), (center_x + 100, h//2), (0, 255, 255), 5)
    elif direction == "Stop":
        cv2.putText(frame, "STOP", (center_x - 50, h//2), cv2.FONT_HERSHEY_SIMPLEX, 
                    2, (0, 0, 255), 5)

    # Direction text
    cv2.putText(frame, f"Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2)

    cv2.imshow('Navigation Path', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
