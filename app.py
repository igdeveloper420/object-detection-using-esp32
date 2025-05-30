import cv2
import numpy as np
import requests
import pyttsx3
from ultralytics import YOLO

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed

# ESP32-CAM IP
URL = 'http://192.168.1.12/cam-hi.jpg'

# Load YOLO model
model = YOLO('yolov8n.pt')  # lightweight model

# For tracking already spoken objects
spoken_labels = set()

def get_image():
    try:
        resp = requests.get(URL, timeout=7)
        img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("❌ Could not fetch image:", e)
        return None

while True:
    frame = get_image()
    if frame is None:
        continue

    frame = cv2.resize(frame, (640, 480))

    # Run detection
    results = model(frame, verbose=False)[0]
    annotated = results.plot()

    # Get detected labels
    labels = [model.names[int(cls)] for cls in results.boxes.cls]

    # Speak out only new objects
    for label in labels:
        if label not in spoken_labels:
            print(f"🗣️ Speaking: {label}")
            engine.say(label)
            engine.runAndWait()
            spoken_labels.add(label)

    # Reset spoken labels occasionally (optional)
    if len(spoken_labels) > 20:
        spoken_labels.clear()

    cv2.imshow("YOLOv8 Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
