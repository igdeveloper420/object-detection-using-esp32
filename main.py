import cv2
import numpy as np
import requests
import pyttsx3
from ultralytics import YOLO
import time

# 🚨 Replace these IPs with your ESP32 settings
URL = 'http://192.168.1.4/cam-hi.jpg'          # ESP32-CAM stream
ESP32_URL = 'http://192.168.1.4/receive'       # ESP32 receive endpoint

# 🧠 Load YOLOv8 model
model = YOLO('yolov8n.pt')  # Use yolov8n.pt, yolov8s.pt etc.

# 🔊 Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# ⏱️ Track last spoken time per label to prevent spamming
spoken_labels_time = {}

def get_image():
    try:
        print("📡 Fetching image from ESP32...")
        resp = requests.get(URL, timeout=7)
        img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            print("❌ Frame decode failed")
        return img
    except Exception as e:
        print("❌ Could not fetch image:", e)
        return None

while True:
    frame = get_image()
    if frame is None:
        continue

    frame = cv2.resize(frame, (640, 480))

    # 🧠 Run YOLOv8 Detection
    results = model(frame, verbose=False)[0]
    annotated = results.plot()

    # 🏷️ Extract labels from result
    labels = [model.names[int(cls)] for cls in results.boxes.cls]

    for label in labels:
        now = time.time()

        # Speak/send only once every 5 seconds per label
        if label not in spoken_labels_time or (now - spoken_labels_time[label]) > 5:
            print(f"🗣️ Speaking & sending to ESP32: {label}")
            try:
                engine.say(label)
                engine.runAndWait()
            except Exception as e:
                print("⚠️ Speech error:", e)

            spoken_labels_time[label] = now

            # Send to ESP32
            try:
                response = requests.get(f"{ESP32_URL}?object={label}")
                print(f"➡️ Sent to ESP32: {response.status_code}")
            except Exception as e:
                print("⚠️ Could not send to ESP32:", e)

    # 🖼️ Show detection window
    cv2.imshow("YOLOv8 Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
