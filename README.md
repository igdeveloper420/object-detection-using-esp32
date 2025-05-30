🧠 YOLOv8 ESP32-CAM Object Detection System
Using Python, OpenCV, and pyttsx3 with Ultralytics YOLOv8

📁 app.py — Basic Object Detection with Voice Alerts
🚀 Overview
A lightweight application that:

Streams frames from an ESP32-CAM.

Detects objects using YOLOv8n.

Speaks object labels using Text-to-Speech (TTS).

Avoids repeating the same label continuously.


🛠️ Core Components

| Component     | Description                                 |
| ------------- | ------------------------------------------- |
| 🧠 Model      | `yolov8n.pt` (YOLOv8 nano - fast and small) |
| 🎤 TTS Engine | `pyttsx3` (offline voice synthesis)         |
| 🎥 Camera     | ESP32-CAM image stream (`/cam-hi.jpg`)      |

🔁 Program Flow
Connect to ESP32-CAM and get the image.

Resize the frame to 640×480.

Run YOLOv8 inference on the frame.

Speak detected labels only once per session.

Clear spoken labels if the list grows too long.

Display the results using OpenCV GUI.

📸 Screenshot Behavior
| Event       | Action                                |
| ----------- | ------------------------------------- |
| 🖼️ Display | Annotated detection window shown live |
| ⏹️ Exit     | Press `q` to quit safely              |

📦 Highlights
| Feature                | Status    |
| ---------------------- | --------- |
| ✅ Lightweight and fast | Supported |
| ✅ Uses TTS             | Supported |
| ✅ Prevents duplicates  | Supported |

⚖️ Comparison Summary
| Feature          | `app.py` ✅           | `main.py` ✅                   |
| ---------------- | -------------------- | ----------------------------- |
| Object Detection | ✅ YOLOv8n            | ✅ YOLOv8n                     |
| ESP32 Triggering | ❌ No                 | ✅ Sends labels to ESP32       |
| Voice Alerts     | ✅ Basic TTS          | ✅ Time-controlled TTS         |
| Spam Prevention  | ❌ Only unique labels | ✅ 5-second cooldown per label |
| Visual Output    | ✅ OpenCV GUI         | ✅ OpenCV GUI                  |

