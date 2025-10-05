# from fastapi import FastAPI
# from ultralytics import YOLO
# import cv2, os
# import numpy as np
# from datetime import datetime
# import mss

# app = FastAPI()
# model = YOLO("yolov8n.pt")  

# SAVE_DIR = "faces"
# os.makedirs(SAVE_DIR, exist_ok=True)
# # ================================================ screen capture ===========================================================================
# # @app.get("/capture")
# # def capture_frame():
# #     """Capture Zoom window (or full screen), detect faces, save cropped faces."""
# #     with mss.mss() as sct:
# #         monitor = sct.monitors[1]  # full screen (change if multi-monitor)
# #         screenshot = np.array(sct.grab(monitor))

# #     frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

# #     results = model(frame)
# #     faces = []

# #     for r in results:
# #         for box in r.boxes.xyxy:
# #             x1, y1, x2, y2 = map(int, box)
# #             face = frame[y1:y2, x1:x2]

# #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
# #             path = f"{SAVE_DIR}/face_{timestamp}.jpg"
# #             cv2.imwrite(path, face)
# #             faces.append(path)

# #     return {"faces": faces}
# # ==================================================== webcam ==============================================================

# @app.get("/capture")
# def capture_webcam():
#     """Capture frame from webcam instead of screen."""
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if not ret:
#         return {"error": "Unable to access webcam"}

#     results = model(frame)
#     faces = []

#     for r in results:
#         for box in r.boxes.xyxy:
#             x1, y1, x2, y2 = map(int, box)
#             face = frame[y1:y2, x1:x2]
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
#             path = f"{SAVE_DIR}/face_{timestamp}.jpg"
#             cv2.imwrite(path, face)
#             faces.append(path)

#     return {"faces": faces}
# ================================================================================================================

from fastapi import FastAPI
from ultralytics import YOLO
import cv2, os
import numpy as np
from datetime import datetime
import mss

app = FastAPI()
model = YOLO("yolov8n.pt")

SAVE_DIR = "faces"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.get("/capture")
def capture_screenshot():
    """Capture screenshot, detect faces, and save cropped ones."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 1 = primary screen
        screenshot = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    results = model(frame)
    faces = []

    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            face = frame[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
            path = f"{SAVE_DIR}/face_{timestamp}.jpg"
            cv2.imwrite(path, face)
            faces.append(path)

    return {"faces": faces, "count": len(faces)}
