from ultralytics import YOLO
import cv2
import cvzone
import random
# import math
import json
import os


with open('config.json') as config_file:
    config = json.load(config_file)

cap = cv2.VideoCapture(config["videoCapture"]["device"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["videoCapture"]["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["videoCapture"]["height"])

model = YOLO(config["paths"]["model_Path"])

classNames = config["classes"]["classNames"]


if cap.isOpened():
    while True:
        ret, frame = cap.read()
        results = model(frame, stream=True)

        target = {
            "w": 0,
            "h": 0,
            "bbox": (0, 0, 0, 0),
            'box': None,
            'conff': 0,
        }
        for r in results:
            boxes = r.boxes
            
            if not len(boxes):
                target = {
                    "w": 0,
                    "h": 0,
                    "bbox": (0, 0, 0, 0),
                    'box': None,
                    'conff': 0,
                }

            for box in boxes:
                # Bounding box

                x1, y1, x2, y2 = box.xyxy[0]
                w, h = int(x2) - int(x1), int(y2) - int(y1)
                bbox = int(x1), int(y1), int(w), int(h)

                conff = round(float(box.conf[0]), 2)

                if (w*h > target['w'] * target['h'] or target['conff'] < conff):
                    target['w'] = w
                    target['h'] = h
                    target['bbox'] = bbox
                    target['box'] = box
                    target['conff'] = conff


            if target['box']:
                cvzone.cornerRect(frame, target['bbox'], l=config["rectSetup"]["length"], t=config["rectSetup"]["thickness"],
                                    colorR=tuple(config["rectSetup"]["rectColor"]))

                # Confidence

                # confidence = math.ceil((box.conf[0] * 100)) / 100
                conff = round(float(target['box'].conf[0]), 2)

                # Class name
                cls = target['box'].cls[0]
                crClass = classNames[int(cls)]
                cvzone.putTextRect(frame, f'{crClass} {conff}', (max(0, int(x1)), max(35, int(y1))),
                                    scale=config["textSetup"]["scale"], thickness=config["textSetup"]["thickness"],
                                    offset=config["textSetup"]["offset"])




        key = cv2.waitKey(1)
        cv2.imshow("Video", frame)
        if key == ord("w"):
            # cv2.imwrite(config["paths"]["saved_Images_path"] + "/saved_Image_{}.jpg".format(str(random.random())), frame)
            pass
        elif key == ord("q"):
            break
        else:
            continue



cap.release()
cv2.destroyAllWindows()


