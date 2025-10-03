"""
hand_gesture_control_opencv.py
Hand gesture recognition with data collection mode using OpenCV only
"""

import cv2
import numpy as np
import time
import os
import json
from datetime import datetime

class HandGestureDetector:
    def __init__(self):
        # Skin color ranges in HSV
        self.lower_skin1 = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin1 = np.array([20, 255, 255], dtype=np.uint8)
        self.lower_skin2 = np.array([170, 20, 70], dtype=np.uint8)
        self.upper_skin2 = np.array([180, 255, 255], dtype=np.uint8)
        
        # Background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
        
        # Data collection
        self.collecting_data = False
        self.data_points = []
        self.current_gesture = "unknown"
        
        # Create data directory
        self.data_dir = "gesture_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Gesture labels
        self.gestures = {
            0: "Fist",
            1: "One",
            2: "Two", 
            3: "Three",
            4: "Four",
            5: "Five",
            "fist": "FORWARD",
            "five": "BACK",
            "two": "LEFT",
            "three": "RIGHT",
            "other": "STOP"
        }
        
        # Performance tracking
        self.frame_count = 0
        self.fps = 0
        self.start_time = time.time()

    def get_skin_mask(self, frame):
        """Create skin color mask"""
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, self.lower_skin1, self.upper_skin1)
        mask2 = cv2.inRange(hsv, self.lower_skin2, self.upper_skin2)
        skin_mask = cv2.bitwise_or(mask1, mask2)
        
        kernel = np.ones((5, 5), np.uint8)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        fg_mask = self.bg_subtractor.apply(blurred)
        combined_mask = cv2.bitwise_and(skin_mask, skin_mask, mask=fg_mask)
        
        return combined_mask

    def find_hand_contour(self, mask):
        """Find hand contour and bounding box"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
        
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        if area < 2000:
            return None, None
        
        x, y, w, h = cv2.boundingRect(largest_contour)
        return largest_contour, (x, y, w, h)

    def extract_features(self, contour, bbox):
        """Extract hand features for gesture recognition"""
        if contour is None:
            return None
        
        features = {}
        
        # Basic contour features
        features['area'] = cv2.contourArea(contour)
        features['perimeter'] = cv2.arcLength(contour, True)
        
        # Bounding box features
        if bbox:
            x, y, w, h = bbox
            features['bbox_ratio'] = w / h if h > 0 else 0
            features['bbox_area'] = w * h
        
        # Convex hull features for finger counting
        try:
            hull = cv2.convexHull(contour, returnPoints=False)
            if len(hull) > 2:
                defects = cv2.convexityDefects(contour, hull)
                if defects is not None:
                    finger_count = 0
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        if d > 10000:
                            finger_count += 1
                    features['finger_count'] = min(finger_count, 5)
                else:
                    features['finger_count'] = 0
            else:
                features['finger_count'] = 0
        except:
            features['finger_count'] = 0
        
        # Hu moments for shape recognition
        moments = cv2.moments(contour)
        if moments['m00'] != 0:
            hu_moments = cv2.HuMoments(moments)
            features['hu_moments'] = [float(m[0]) for m in hu_moments]
        
        return features

    def classify_gesture(self, features):
        """Classify gesture based on extracted features"""
        if features is None:
            return "STOP", "No Hand"
        
        finger_count = features.get('finger_count', 0)
        
        # Map finger count to gestures
        if finger_count == 0:
            return "FORWARD", "Fist"
        elif finger_count == 5:
            return "BACK", "Open Palm"
        elif finger_count == 2:
            return "LEFT", "Two Fingers"
        elif finger_count == 3:
            return "RIGHT", "Three Fingers"
        else:
            return "STOP", f"Fingers:{finger_count}"

    def save_data_point(self, features, gesture_label):
        """Save data point for training"""
        if features and self.collecting_data:
            data_point = {
                'timestamp': datetime.now().isoformat(),
                'features': features,
                'gesture': gesture_label,
                'finger_count': features.get('finger_count', 0)
            }
            self.data_points.append(data_point)
            
            # Save periodically
            if len(self.data_points) % 10 == 0:
                self.save_collected_data()

    def save_collected_data(self):
        """Save all collected data to file"""
        if self.data_points:
            filename = f"{self.data_dir}/gesture_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.data_points, f, indent=2)
            print(f"Saved {len(self.data_points)} data points to {filename}")

    def calculate_fps(self):
        """Calculate and return current FPS"""
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            end_time = time.time()
            self.fps = 30 / (end_time - self.start_time)
            self.start_time = end_time
        return self.fps

    def draw_display(self, frame, contour, bbox, gesture, finger_gesture, features):
        """Draw the main display similar to the screenshot"""
        h, w = frame.shape[:2]
        
        # Create semi-transparent overlay for info panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw hand visualization
        if contour is not None and bbox is not None:
            # Draw contour in green
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Draw bounding box in blue
            x, y, w_bbox, h_bbox = bbox
            cv2.rectangle(frame, (x, y), (x + w_bbox, y + h_bbox), (255, 0, 0), 2)
            
            # Draw convex hull in red
            hull = cv2.convexHull(contour)
            cv2.drawContours(frame, [hull], -1, (0, 0, 255), 1)
            
            # Draw center point
            center_x = x + w_bbox // 2
            center_y = y + h_bbox // 2
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # Display information in the style of the screenshot
        y_offset = 30
        line_height = 25
        
        # FPS
        cv2.putText(frame, f"FPS: {self.fps:.2f}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y_offset += line_height
        
        # Finger Gesture
        cv2.putText(frame, f"Finger Gesture: {finger_gesture}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += line_height
        
        # Model Mode
        mode_text = "Logging Key Point" if self.collecting_data else "Detection Mode"
        mode_color = (0, 255, 0) if self.collecting_data else (255, 255, 255)
        cv2.putText(frame, f"MODEL: {mode_text}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)
        y_offset += line_height
        
        # Number of data points if collecting
        if self.collecting_data:
            cv2.putText(frame, f"NUM: {len(self.data_points)}", (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_offset += line_height
        
        # Command status
        cv2.putText(frame, f"Command: {gesture}", (w - 200, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Hand status
        hand_status = "Right: Open" if contour is not None else "Right: Closed"
        status_color = (0, 255, 0) if contour is not None else (0, 0, 255)
        cv2.putText(frame, hand_status, (w - 200, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Instructions
        instructions = [
            "Press 'K': Start/Stop Data Collection",
            "Press '1-5': Set Gesture Label", 
            "Press 'R': Reset Background",
            "Press 'Q': Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, h - 80 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        return frame

def main():
    detector = HandGestureDetector()
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Hand Gesture Control System")
    print("=" * 50)
    print("1. Learning data collection")
    print("   Press 'K' to enter the mode to save key points")
    print("   Press '1-5' to set gesture label during collection")
    print("2. Real-time gesture recognition")
    print("3. Press 'Q' to quit")
    print("=" * 50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        
        # Calculate FPS
        fps = detector.calculate_fps()
        
        # Process frame
        skin_mask = detector.get_skin_mask(frame)
        contour, bbox = detector.find_hand_contour(skin_mask)
        features = detector.extract_features(contour, bbox)
        
        # Classify gesture
        gesture, finger_gesture = detector.classify_gesture(features)
        
        # Save data if in collection mode
        if detector.collecting_data:
            detector.save_data_point(features, detector.current_gesture)
        
        # Draw display
        frame = detector.draw_display(frame, contour, bbox, gesture, finger_gesture, features)
        
        # Show mask window
        mask_display = cv2.resize(skin_mask, (320, 240))
        cv2.imshow("Hand Mask", mask_display)
        cv2.imshow("Hand Gesture Control", frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('k'):
            detector.collecting_data = not detector.collecting_data
            if detector.collecting_data:
                print("Started data collection mode")
                detector.data_points = []  # Clear previous data
            else:
                print("Stopped data collection mode")
                detector.save_collected_data()
        elif key == ord('r'):
            detector.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
            print("Background reset")
        elif key in [ord(str(i)) for i in range(1, 6)]:
            gesture_num = int(chr(key))
            detector.current_gesture = detector.gestures.get(gesture_num, f"Gesture_{gesture_num}")
            print(f"Set gesture label to: {detector.current_gesture}")
    
    # Save any remaining data
    if detector.collecting_data:
        detector.save_collected_data()
    
    cap.release()
    cv2.destroyAllWindows()
    print("System shutdown complete")

if __name__ == "__main__":
    main()