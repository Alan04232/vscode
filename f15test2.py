import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    print("Path Prediction System Running - Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame")
            break
        
        # Flip frame horizontally for mirror view
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        
        # Create a region of interest (ROI) - lower half of the frame
        roi = frame[height//2:height, :]
        
        # Convert to grayscale and detect edges
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=50, maxLineGap=100)
        
        # Initialize path points
        path_points = []
        
        if lines is not None:
            # Filter and average lines to find the central path
            left_lines = []
            right_lines = []
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Avoid division by zero
                
                # Classify as left or right line based on slope
                if slope < -0.5:  # Left line
                    left_lines.append(line[0])
                elif slope > 0.5:  # Right line
                    right_lines.append(line[0])
            
            # Calculate average left and right lines
            if left_lines:
                avg_left = np.mean(left_lines, axis=0)
                x1, y1, x2, y2 = avg_left.astype(int)
                cv2.line(roi, (x1, y1), (x2, y2), (255, 0, 0), 3)
                path_points.append(((x1 + x2) // 2, (y1 + y2) // 2))
            
            if right_lines:
                avg_right = np.mean(right_lines, axis=0)
                x1, y1, x2, y2 = avg_right.astype(int)
                cv2.line(roi, (x1, y1), (x2, y2), (0, 0, 255), 3)
                path_points.append(((x1 + x2) // 2, (y1 + y2) // 2))
        
        # Predict path (simple version)
        if len(path_points) >= 2:
            # Calculate midpoint between detected lines
            start_point = (width // 2, height)
            mid_x = (path_points[0][0] + path_points[1][0]) // 2
            mid_y = (path_points[0][1] + path_points[1][1]) // 2
            end_point = (mid_x, mid_y - height//4)  # Extend path upward
            
            # Draw predicted path
            cv2.line(frame, start_point, (mid_x, mid_y), (0, 255, 0), 5)
            cv2.line(frame, (mid_x, mid_y), end_point, (0, 255, 255), 5)
            
            # Add arrow head
            cv2.arrowedLine(frame, (mid_x, mid_y), end_point, (0, 255, 255), 5, tipLength=0.3)
            
            # Determine curve direction
            if mid_x > width // 2 + 50:
                direction = "Right Curve"
            elif mid_x < width // 2 - 50:
                direction = "Left Curve"
            else:
                direction = "Straight"
            
            cv2.putText(frame, f"Predicted: {direction}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Show the result
        cv2.imshow('Path Prediction', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()