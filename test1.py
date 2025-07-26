import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(img, mask)

def average_slope_intercept(lines):
    left_lines = []
    right_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        if x2 - x1 == 0:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if slope < -0.5:
            left_lines.append((slope, intercept))
        elif slope > 0.5:
            right_lines.append((slope, intercept))

    left_avg = np.mean(left_lines, axis=0) if left_lines else None
    right_avg = np.mean(right_lines, axis=0) if right_lines else None

    return left_avg, right_avg

def make_line_points(y1, y2, line_params):
    slope, intercept = line_params
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, y1, x2, y2)

def detect_lanes(image):
    height, width = image.shape[:2]
    roi_vertices = np.array([[
        (0, height),
        (width // 2 - 50, height // 2 + 40),
        (width // 2 + 50, height // 2 + 40),
        (width, height)
    ]], dtype=np.int32)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    cropped_edges = region_of_interest(edges, roi_vertices)
    lines = cv2.HoughLinesP(cropped_edges, 2, np.pi/180, 100, minLineLength=50, maxLineGap=50)

    direction = "No Path"
    lane_image = image.copy()

    if lines is not None:
        left_avg, right_avg = average_slope_intercept(lines)

        y1 = image.shape[0]
        y2 = int(y1 * 0.6)

        left_line = right_line = None

        if left_avg is not None:
            left_line = make_line_points(y1, y2, left_avg)
            cv2.line(lane_image, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (255, 0, 0), 5)
        
        if right_avg is not None:
            right_line = make_line_points(y1, y2, right_avg)
            cv2.line(lane_image, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (0, 255, 0), 5)

        # Path decision logic
        if left_line and right_line:
            mid_lane = ((left_line[2] + right_line[2]) // 2)
            deviation = mid_lane - width // 2

            if deviation < -40:
                direction = "Turn Left"
            elif deviation > 40:
                direction = "Turn Right"
            else:
                direction = "Go Straight"
        elif left_line:
            direction = "Turn Right (only left lane)"
        elif right_line:
            direction = "Turn Left (only right lane)"

    # Show the decision
    cv2.putText(lane_image, f"Direction: {direction}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return lane_image

# Main execution
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    result = detect_lanes(frame)
    cv2.imshow("Advanced Lane Navigation", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
