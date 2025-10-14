
import cv2
import socket
import pickle
import struct

# Connect to WSL server (same PC, localhost)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Serialize frame and send to WSL
    data = pickle.dumps(frame)
    message = struct.pack("Q", len(data)) + data
    client_socket.sendall(message)

    # Receive processed frame back from WSL
    data = b""
    payload_size = struct.calcsize("Q")
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    data = data[payload_size:]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    processed_frame = pickle.loads(frame_data)

    cv2.imshow("Face Detection (WSL)", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
client_socket.close()
