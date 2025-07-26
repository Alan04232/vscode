import sys
import cv2
import threading
import speech_recognition as sr
import pyttsx3
from PyQt5 import QtWidgets, QtGui, QtCore

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Voice output
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Voice input
def listen_and_respond():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command: {command}")
        speak(f"You said {command}")
        return command
    except:
        speak("Sorry, I didn't catch that.")
        return None

# GUI Application with webcam
class CarAssistantApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Car Assistant")
        self.setGeometry(100, 100, 800, 600)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(10, 10, 640, 480)
        self.label.setStyleSheet("border: 2px solid black;")

        self.statusLabel = QtWidgets.QLabel("Status: Waiting...", self)
        self.statusLabel.setGeometry(10, 500, 780, 40)
        self.statusLabel.setStyleSheet("font-size: 16px;")

        self.button = QtWidgets.QPushButton("Give Voice Command", self)
        self.button.setGeometry(660, 50, 120, 40)
        self.button.clicked.connect(self.handle_voice)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Simulate path prediction with edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            edges = cv2.Canny(gray, 100, 200)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_RGB2BGR)

            # Convert to Qt format
            image = QtGui.QImage(edges_rgb.data, edges_rgb.shape[1], edges_rgb.shape[0],
                                 edges_rgb.strides[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(image)
            self.label.setPixmap(pix)

    def handle_voice(self):
        self.statusLabel.setText("Status: Listening...")
        thread = threading.Thread(target=self.listen_in_thread)
        thread.start()

    def listen_in_thread(self):
        command = listen_and_respond()
        if command:
            self.statusLabel.setText(f"Status: Heard - {command}")
        else:
            self.statusLabel.setText("Status: Could not understand.")

    def closeEvent(self, event):
        self.cap.release()

# Main
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = CarAssistantApp()
    mainWin.show()
    sys.exit(app.exec_())
